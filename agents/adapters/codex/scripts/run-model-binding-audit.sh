#!/bin/sh

set -eu

AUDIT_CODEX_BIN="${CODEX_MODEL_AUDIT_BIN:-/Users/jungcho/.local/bin/codex}"
AUDIT_REPO_ROOT="${CODEX_MODEL_AUDIT_REPO:-/Users/jungcho/Projects/ai-assets}"
AUDIT_LOG_DIR="${CODEX_MODEL_AUDIT_LOG_DIR:-/Users/jungcho/Library/Logs/codex-model-binding-audit}"
AUDIT_PROFILE="model-binding-audit"
AUDIT_PROFILE_PATH="$AUDIT_REPO_ROOT/agents/adapters/codex/profiles/model-binding-audit.config.toml"
AUDIT_DOCS_HELPER="${CODEX_MODEL_AUDIT_DOCS_HELPER:-/Users/jungcho/.codex/skills/.system/openai-docs/scripts/fetch-codex-manual.mjs}"
AUDIT_PROMPT_BASE='Run the read-only Codex model-binding audit defined in agents/adapters/codex/model-binding-audit.md. Use $openai-docs. You are already inside the audit invocation: do not run codex or codex exec recursively. Remain in the root agent and do not invoke subagents. Treat the generated canonical binding manifest below as exact local input, verify official lifecycle sources, and return only the audit status and output contract with the status value on the same line as Status:.'

mkdir -p "$AUDIT_LOG_DIR/runs"

RUN_ID=$(date '+%Y%m%dT%H%M%S%z')
STARTED_AT=$(date '+%Y-%m-%dT%H:%M:%S%z')
REPORT_TMP=$(mktemp "$AUDIT_LOG_DIR/.report.XXXXXX")
STDOUT_TMP=$(mktemp "$AUDIT_LOG_DIR/.stdout.XXXXXX")
STDERR_TMP=$(mktemp "$AUDIT_LOG_DIR/.stderr.XXXXXX")
SOURCE_PREFLIGHT_TMP=$(mktemp "$AUDIT_LOG_DIR/.source-preflight.XXXXXX")

cleanup() {
  rm -f "$REPORT_TMP" "$STDOUT_TMP" "$STDERR_TMP" "$SOURCE_PREFLIGHT_TMP"
}

trap cleanup EXIT HUP INT TERM

REPORT_PATH="$AUDIT_LOG_DIR/runs/$RUN_ID.report.txt"
STDOUT_PATH="$AUDIT_LOG_DIR/runs/$RUN_ID.stdout.log"
STDERR_PATH="$AUDIT_LOG_DIR/runs/$RUN_ID.stderr.log"
SOURCE_PREFLIGHT_PATH="$AUDIT_LOG_DIR/runs/$RUN_ID.source-preflight.log"
LATEST_REPORT="$AUDIT_LOG_DIR/latest-report.txt"
LATEST_STDOUT="$AUDIT_LOG_DIR/latest-stdout.log"
LATEST_STDERR="$AUDIT_LOG_DIR/latest-stderr.log"
LATEST_SOURCE_PREFLIGHT="$AUDIT_LOG_DIR/latest-source-preflight.log"
LATEST_STATUS="$AUDIT_LOG_DIR/latest-status.txt"
ATTENTION_SENTINEL="$AUDIT_LOG_DIR/attention-required.txt"
ACTUAL_MODEL="unknown"
SOURCE_PREFLIGHT_STATUS="unavailable"
EXPECTED_MODEL=""
if [ -f "$AUDIT_PROFILE_PATH" ]; then
  EXPECTED_MODEL=$(sed -n 's/^model[[:space:]]*=[[:space:]]*"\([^"]*\)".*/\1/p' "$AUDIT_PROFILE_PATH" | head -n 1)
fi
BINDING_MANIFEST=""
if [ -d "$AUDIT_REPO_ROOT/agents/adapters/codex/custom-agents" ] && \
  [ -d "$AUDIT_REPO_ROOT/agents/adapters/codex/profiles" ]; then
  BINDING_MANIFEST=$(
    find "$AUDIT_REPO_ROOT/agents/adapters/codex/custom-agents" \
      "$AUDIT_REPO_ROOT/agents/adapters/codex/profiles" \
      -type f -name '*.toml' -print | sort | while IFS= read -r binding_file; do
        printf '[%s]\n' "${binding_file#"$AUDIT_REPO_ROOT"/}"
        sed -n -E '/^(name|model|model_reasoning_effort|sandbox_mode|approval_policy)[[:space:]]*=/p; /^\[agents\]$/p; /^enabled[[:space:]]*=/p' "$binding_file"
        printf '\n'
      done
  )
fi

MANUAL_PATH=""
OUTLINE_PATH=""
if [ -f "$AUDIT_DOCS_HELPER" ] && command -v node >/dev/null 2>&1; then
  if node "$AUDIT_DOCS_HELPER" >"$SOURCE_PREFLIGHT_TMP" 2>>"$STDERR_TMP"; then
    MANUAL_PATH=$(sed -n 's/^Manual path:[[:space:]]*//p' "$SOURCE_PREFLIGHT_TMP" | head -n 1)
    OUTLINE_PATH=$(sed -n 's/^Outline path:[[:space:]]*//p' "$SOURCE_PREFLIGHT_TMP" | head -n 1)
    if [ -r "$MANUAL_PATH" ] && [ -r "$OUTLINE_PATH" ]; then
      SOURCE_PREFLIGHT_STATUS="verified"
    fi
  fi
fi

if [ "$SOURCE_PREFLIGHT_STATUS" = "verified" ]; then
  SOURCE_CONTEXT=$(printf 'The openai-docs helper freshness-checked the current official Codex manual before this run. Use targeted searches and reads in these files as the first source for model, changelog, and subagent lifecycle claims:\nManual: %s\nOutline: %s\nUse live official search only for material gaps.' "$MANUAL_PATH" "$OUTLINE_PATH")
else
  SOURCE_CONTEXT='The official Codex manual preflight was unavailable. Check the required official sources with native search and return SOURCE_UNAVAILABLE if they cannot be verified.'
fi

EXACT_MODEL_EVIDENCE=""
if [ "$SOURCE_PREFLIGHT_STATUS" = "verified" ] && command -v rg >/dev/null 2>&1; then
  EXACT_MODEL_EVIDENCE=$(
    printf '%s\n' "$BINDING_MANIFEST" \
      | sed -n 's/^model[[:space:]]*=[[:space:]]*"\([^"]*\)".*/\1/p' \
      | sort -u \
      | while IFS= read -r bound_model; do
          [ -n "$bound_model" ] || continue
          printf '[exact official-manual matches for %s]\n' "$bound_model"
          rg -n -i -F -C 4 -- "$bound_model" "$MANUAL_PATH" | head -n 120 || true
          printf '\n'
        done
  )
fi
if [ -z "$EXACT_MODEL_EVIDENCE" ]; then
  EXACT_MODEL_EVIDENCE='No exact-match evidence was pre-extracted; inspect required official sources directly.'
fi

AUDIT_PROMPT=$(printf '%s\n\n%s\n\nCanonical binding manifest generated from the source TOMLs:\n%s\n\nPre-extracted exact-binding evidence from the freshness-checked official manual:\n%s' \
  "$AUDIT_PROMPT_BASE" "$SOURCE_CONTEXT" "$BINDING_MANIFEST" "$EXACT_MODEL_EVIDENCE")

persist_outputs() {
  cp "$REPORT_TMP" "$REPORT_PATH"
  cp "$STDOUT_TMP" "$STDOUT_PATH"
  cp "$STDERR_TMP" "$STDERR_PATH"
  cp "$SOURCE_PREFLIGHT_TMP" "$SOURCE_PREFLIGHT_PATH"
  cp "$REPORT_TMP" "$LATEST_REPORT"
  cp "$STDOUT_TMP" "$LATEST_STDOUT"
  cp "$STDERR_TMP" "$LATEST_STDERR"
  cp "$SOURCE_PREFLIGHT_TMP" "$LATEST_SOURCE_PREFLIGHT"
}

write_status() {
  status_value=$1
  detail_value=$2
  completed_at=$(date '+%Y-%m-%dT%H:%M:%S%z')
  printf 'Status: %s\nStarted at: %s\nCompleted at: %s\nProfile: %s\nExpected model: %s\nActual model: %s\nOfficial source preflight: %s\nReport: %s\nDetails: %s\n' \
    "$status_value" "$STARTED_AT" "$completed_at" "$AUDIT_PROFILE" "$EXPECTED_MODEL" "$ACTUAL_MODEL" "$SOURCE_PREFLIGHT_STATUS" \
    "$REPORT_PATH" "$detail_value" \
    >"$LATEST_STATUS"
}

write_attention() {
  status_value=$1
  detail_value=$2
  detected_at=$(date '+%Y-%m-%dT%H:%M:%S%z')
  printf 'Status: %s\nDetected at: %s\nReport: %s\nNext action: %s\n' \
    "$status_value" "$detected_at" "$REPORT_PATH" "$detail_value" \
    >"$ATTENTION_SENTINEL"
}

if [ -z "$EXPECTED_MODEL" ]; then
  printf 'Audit profile has no explicit model binding: %s\n' "$AUDIT_PROFILE_PATH" >"$STDERR_TMP"
  persist_outputs
  write_status "AUDIT_RUN_FAILED" "Audit profile binding is missing; no model was invoked."
  write_attention "AUDIT_RUN_FAILED" "Restore an explicit reviewed model binding in the canonical audit profile."
  printf 'Status: AUDIT_RUN_FAILED\nReport: %s\n' "$REPORT_PATH" >&2
  exit 4
fi

if [ ! -x "$AUDIT_CODEX_BIN" ]; then
  printf 'Codex executable is not available at %s\n' "$AUDIT_CODEX_BIN" >"$STDERR_TMP"
  persist_outputs
  write_status "AUDIT_RUN_FAILED" "Codex executable unavailable; no fallback was attempted."
  write_attention "AUDIT_RUN_FAILED" "Restore the configured Codex executable, then run the audit manually."
  printf 'Status: AUDIT_RUN_FAILED\nReport: %s\n' "$REPORT_PATH" >&2
  exit 4
fi

if "$AUDIT_CODEX_BIN" --search --sandbox read-only --ask-for-approval never \
  exec --profile "$AUDIT_PROFILE" --ephemeral --strict-config --color never \
  --cd "$AUDIT_REPO_ROOT" --output-last-message "$REPORT_TMP" \
  "$AUDIT_PROMPT" >"$STDOUT_TMP" 2>>"$STDERR_TMP"; then
  ACTUAL_MODEL=$(sed -n 's/^model:[[:space:]]*//p' "$STDERR_TMP" | head -n 1)
  if [ -z "$ACTUAL_MODEL" ]; then
    ACTUAL_MODEL="unknown"
  fi
  AUDIT_STATUS=$(awk '
    /^Status:[[:space:]]*[A-Z_]+[[:space:]]*$/ {
      sub(/^Status:[[:space:]]*/, "")
      sub(/[[:space:]]*$/, "")
      print
      exit
    }
    /^Status:[[:space:]]*$/ {
      if (getline > 0) {
        sub(/^[[:space:]]*/, "")
        sub(/[[:space:]]*$/, "")
        print
      }
      exit
    }
  ' "$REPORT_TMP")
  persist_outputs

  if [ "$ACTUAL_MODEL" != "$EXPECTED_MODEL" ]; then
    write_status "AUDIT_MODEL_MISMATCH" "The runtime model differed from the explicit profile binding; the audit result was not accepted."
    write_attention "AUDIT_MODEL_MISMATCH" "Review runtime model resolution with the configured primary agent. Do not accept or substitute the binding automatically."
    printf 'Status: AUDIT_MODEL_MISMATCH\nReport: %s\n' "$REPORT_PATH" >&2
    exit 6
  fi

  case "$AUDIT_STATUS" in
    NO_BINDING_CHANGE)
      write_status "$AUDIT_STATUS" "No binding review is required."
      rm -f "$ATTENTION_SENTINEL"
      printf 'Status: %s\nReport: %s\n' "$AUDIT_STATUS" "$REPORT_PATH"
      ;;
    REVIEW_REQUIRED)
      write_status "$AUDIT_STATUS" "A competence-qualified primary-model review is required; no replacement was applied."
      write_attention "$AUDIT_STATUS" "Review the report with the configured primary agent before changing any binding."
      printf 'Status: %s\nReport: %s\n' "$AUDIT_STATUS" "$REPORT_PATH"
      ;;
    SOURCE_UNAVAILABLE)
      write_status "$AUDIT_STATUS" "Required official sources were unavailable; no binding conclusion was made."
      write_attention "$AUDIT_STATUS" "Restore official-source access and rerun the audit; do not infer that bindings are current."
      printf 'Status: %s\nReport: %s\n' "$AUDIT_STATUS" "$REPORT_PATH" >&2
      exit 2
      ;;
    *)
      write_status "INVALID_AUDIT_OUTPUT" "The model completed but did not return a recognized audit status."
      write_attention "INVALID_AUDIT_OUTPUT" "Inspect the report and rerun after correcting the audit contract."
      printf 'Status: INVALID_AUDIT_OUTPUT\nReport: %s\n' "$REPORT_PATH" >&2
      exit 5
      ;;
  esac
else
  ACTUAL_MODEL=$(sed -n 's/^model:[[:space:]]*//p' "$STDERR_TMP" | head -n 1)
  if [ -z "$ACTUAL_MODEL" ]; then
    ACTUAL_MODEL="unknown"
  fi
  persist_outputs

  if grep -Eiq 'unknown model|model[^[:cntrl:]]*(not available|unavailable|not found|unsupported|does not exist)|access[^[:cntrl:]]*model[^[:cntrl:]]*(denied|unavailable)' "$STDERR_TMP"; then
    FAILURE_STATUS="AUDIT_MODEL_UNAVAILABLE"
    FAILURE_DETAIL="The explicitly pinned audit model was unavailable; no fallback model was attempted."
    FAILURE_ACTION="Review the audit profile binding with the configured primary agent. Do not substitute automatically."
    FAILURE_EXIT=3
  else
    FAILURE_STATUS="AUDIT_RUN_FAILED"
    FAILURE_DETAIL="The Codex audit command failed; no fallback model was attempted."
    FAILURE_ACTION="Inspect the stderr log and rerun the exact command manually."
    FAILURE_EXIT=4
  fi

  write_status "$FAILURE_STATUS" "$FAILURE_DETAIL"
  write_attention "$FAILURE_STATUS" "$FAILURE_ACTION"
  printf 'Status: %s\nReport: %s\nStderr: %s\n' \
    "$FAILURE_STATUS" "$REPORT_PATH" "$STDERR_PATH" >&2
  exit "$FAILURE_EXIT"
fi
