# Consumer-repository artifacts

## Contents

- [Choose the owner](#choose-the-owner)
- [Layout and file roles](#layout-and-file-roles)
- [Generate and refresh](#generate-and-refresh)
- [Git, docs and feedback](#git-docs-and-feedback)
- [Retain, move and clean up](#retain-move-and-clean-up)

## Choose the owner

Use **`<repo>/.artifacts/ui-atlas/`** by default. Resolve the repository/project
root deliberately; do not derive it from whichever directory the agent happened
to start in. Use that root as `--source-root` and declare source files relative
to it. A monorepo can keep several atlas IDs in this one workspace.

Resolve exceptions in this order:

1. The user's explicit destination and preservation instructions.
2. Applicable repository rules or an existing, clearly owned atlas location.
3. The default above.

Pass an alternative owner through `--workspace`. Keep the same internal layout.
Do not migrate existing observations just to adopt the default. An explicit
`--out` is a lower-level escape hatch for one new run directory; it bypasses
workspace initialization, ignore setup and the entry catalog. Its caller owns
those responsibilities.

This is the skill's consumer-output convention, independent of any harness.
The reusable skill package stays at its installed/canonical owner. Do not copy
private product observations into the reusable asset repository or vendor the
whole skill into each consumer repo.

The hidden `.artifacts/` parent separates generated observations from product
source and maintained documentation. The `ui-atlas/` child gives recipes, runs
and feedback one identifiable owner without adding a product feature directory
at the repository root. It is a storage convention, not a harness dependency.

## Layout and file roles

```text
<repo>/.artifacts/ui-atlas/
  .gitignore                 # excludes the whole local workspace
  workspace.json             # ownership/schema marker, no product configuration
  index.html                 # opens a topic; menu map includes unassigned/history when present
  navigation.json            # authored product/topic/feature order and state ownership
  topics/                    # generated topic canvases; original observations stay in runs/
  recipes/
    <atlas-id>/
      recipe.json            # stable journeys, state IDs and declared dependencies
      fixtures/              # synthetic inputs and optional isolated-app launcher
  runs/
    <UTC>-<atlas-id>-<unique>/
      atlas.json             # observation manifest, hashes, conditions and failures
      index.html             # self-contained, selectable DOM canvas
      frames/*.html          # original materialized DOM used for rebuilding
  notes/
    <atlas-id>/               # exported review JSON; keep distinct dated exports
  tmp/
    <task-id>/               # disposable browser/server runtime or staging
```

`init` creates the owner, ignore file, role directories and entry HTML. It refuses
a nonempty directory without the workspace marker. Repeating it preserves
recipes, notes and runs. It does not invent a recipe. When an app already owns
stories, fixtures or recipes, reference those originals instead of copying them;
declare their relevant dependencies. Recipe response files and `support_files`
must remain inside that recipe's directory. The workspace's `recipes/` is the
default owner for atlas-specific inputs when no app owner exists.

Each capture gets a new run directory. Without a topic map, the workspace entry
opens the last selected atlas directly, or its first available sheet when no saved
choice is available.
The sheet selector sits above the screen/element/opinion tabs; its full-catalog
dialog lists the latest readable attempts and earlier runs, labels partial failures
and capture-time source-check status, and retains incomplete-run diagnostics.
An explicitly selected historical run remains distinct from an atlas's latest run.
The catalog does not replace
the last successful evidence with a claim of success. A run without a manifest
or built canvas is listed as generating/interrupted. A malformed or unreadable
manifest is listed separately with its error; its files are preserved and it
does not block unrelated/new runs. Capture publishes complete manifests by
atomic replacement, so a failed write cannot truncate an existing manifest.
Declared unknown, unimplemented
and not-applicable states remain coverage information; a completed recipe run is
not exhaustive app validation. The catalog is derived from retained run files;
refresh it after manual moves or pruning. Concurrent runs keep separate outputs;
refresh the catalog after both finish if their entry updates overlap. With no
readable sheet or JavaScript disabled, the entry retains a plain catalog fallback.
An older viewer without the sheet-selection bridge needs a viewer-only `build`
from its retained manifest; a connection failure exposes the fallback and its
standalone links instead of inventing a replacement observation.

With an authored [menu topic map](menu-topics.md), the workspace composes related
observations into product-ordered topic canvases. It preserves source manifests,
identities, original feedback namespaces and retained-run access. Viewport and
state variants stay under their feature. Fully mapped latest captures remain
backing inputs without duplicate menu entries; only unassigned captures and
retained previous runs need a separate disclosure. Omit it when empty.
Without a topic map the existing sheet entry behavior remains available.

The workspace hosts sheets without reflowing their fixed app viewports. Sheet
selection and the last-choice preference belong to the workspace; each sheet
keeps its own inspection state, draft ownership and pending note writes while
mounted. Switching retains sheets with unsaved work. Inactive clean sheets use a
bounded cache; eviction recreates transient inspection state when they reopen
from their original HTML. Saved opinions stay under their existing
atlas identity. Drafts and failed writes are still tab memory, not a durable backup.
The unsaved-work guard also covers inactive sheets. A standalone run continues
to open independently and does not show a disconnected workspace selector.

## Generate and refresh

In these commands, `/path/to/ui-atlas` is the installed skill package, and the
current directory is the deliberately selected consumer repo root:

```sh
python /path/to/ui-atlas/scripts/atlas.py init --source-root .
# Author recipes/main/recipe.json from the app, then start its isolated fixture server.
python /path/to/ui-atlas/scripts/capture.py \
  .artifacts/ui-atlas/recipes/main/recipe.json \
  --source-root . --base-url http://127.0.0.1:8000
```

Omitting `--out` selects the managed workspace. Add `--workspace /chosen/owner`
to both commands for a custom destination. The runner prints the new canvas and
the stable entry path. It needs the optional browser dependencies described in
[DOM states and artifacts](capture-and-artifacts.md); `init`, `catalog`, `check`
and `build` use only Python's standard library.

```sh
python /path/to/ui-atlas/scripts/atlas.py check \
  .artifacts/ui-atlas/runs/<run>/atlas.json
python /path/to/ui-atlas/scripts/atlas.py catalog .artifacts/ui-atlas
```

Check declared source, recipe and support hashes when resuming. Source changes
need a new recipe run. A viewer-only rebuild can reuse matching recorded DOM;
write it to a distinct HTML name if the old viewer is still comparison evidence.
Rebuilding does not observe the app again. A changed inspection bridge marks
old notes for reconsideration even when the app has not changed.

## Git, docs and feedback

- Keep generated observations, local recipes/fixtures, notes and runtime files
  ignored by default. The workspace's own `.gitignore` contains `*`; it neither
  changes the repository's root ignore rules nor untracks already tracked files.
  Check the actual Git status when adopting an existing location. Do not force-add
  outputs or infer publication permission from local generation.
- `docs/` is for deliberately maintained screen explanations, reviewed decisions
  or a short pointer to the local entry path when the team needs one. Do not
  automatically put multi-megabyte generated canvases, raw DOM or fixture runtimes
  under documentation, and do not create a second copy there.
- To share reproducible **synthetic** recipes in Git, explicitly promote them to
  the app's existing test/story owner, or `tests/ui-atlas/` when that fits its
  conventions. Keep generated runs ignored. Review fixture/source contents at
  the publication boundary; the helper never stages, commits or uploads them.
- Saved viewer notes use browser storage and export/import JSON. Unsaved textarea
  drafts stay bound to their state and element during navigation but live only
  in that tab; save them as notes before exporting. Put downloaded exports under
  `notes/<atlas-id>/`; a standalone HTML page cannot silently write that folder.
  Keep multiple exports when they contain distinct work. An imported/reviewed
  note is not approval to edit the app.
  A failed browser save leaves pending note edits/deletions in memory across
  later operations and other-tab updates; later edits or the file-menu retry
  attempt them again. Export added/updated opinions before closing when storage
  remains unavailable. The file is an opinion list, not a deletion log: retry a
  failed deletion before closing, or delete that opinion again later. Importing
  does not delete browser notes omitted from the file. Same-ID differences are
  reviewed explicitly before import, so an older export cannot silently replace
  current work. This recovery buffer is not durable storage and does not include
  unsubmitted textarea drafts. See [feedback behavior](capture-and-artifacts.md#canvas-and-feedback)
  for conflict, cancellation and retry details.

## Retain, move and clean up

Keep recipes/fixtures and exported feedback for reuse. Retain prior runs while
notes, comparisons, decisions or the user's instructions depend on them. The
helper does **not** auto-prune runs, so storage grows with each refresh. When
cleanup is requested, identify obsolete run directories and their dependencies,
preserve required evidence, remove only the selected owned directories, then
refresh the catalog. Never delete an older run merely because a newer one exists.

A complete topic map is a presentation reorganization, not a transfer of all
source data: rebuilding topics and opening their full Payload manifests still
depend on the selected source runs and materialized DOM. Keep those inputs unless
an expressly requested independent-data migration has moved and verified every
consumer. To remove superseded runs under cleanup authorization:

- Resolve the current selected runs and compare every retired atlas/state pair
  against a retained primary owner, including failures and qualified gaps. Count
  equality or matching state names alone is insufficient: inspect changed source,
  recipe, conditions and state results, and account for intentional corrections.
- Verify actual topic inspection, payload links, replay inputs, regeneration and
  the original feedback namespaces/identities. Preserve missing-frame opinions,
  staleness, drafts and failed-save recovery. Do not infer that browser notes were
  transferred from a canvas rebuild or a synthetic compatibility check.
- Resolve unique prior evidence and references needed by notes, comparisons or
  decisions. Preserve their required contents under an existing owner or keep
  that run; update current references and record retirement without rewriting
  earlier verification as current evidence.
- Stop users of the exact retired paths, recheck selected inputs, remove only
  the identified obsolete directories and regenerate the workspace. Verify that
  all current states and source links still work. A removed explicit run must
  report missing evidence rather than redirect to a supposedly equivalent run.

Do not retain a full duplicate migration/archive by default once its purpose has
ended. Keep the minimal required evidence and reusable inputs at their actual
owner, and report exactly what was removed and what remains necessary.

Use one task-owned subdirectory under `tmp/` (or an equivalent task-owned OS
temporary directory) for isolated runtime data. Stop owned servers/browsers and
remove that exact scratch after validation and transfer of needed results.
Do not recursively empty a shared `tmp/`, and do not treat saved runs as scratch.
If diagnosis must continue later, retain only the needed files with their owner
and cleanup condition. Durable recipes must not depend on temporary ports,
profiles, databases or paths.

To move an atlas, copy its owner with recipes/support files, required run DOM and
notes; open the moved entry and import exported notes. HTML is standalone, but
replay and freshness checks also need the matching app source and environment.
If source or recipe locations changed, supply both current locators explicitly:

```sh
python /path/to/ui-atlas/scripts/atlas.py check /moved/run/atlas.json \
  --source-root /moved/app --recipe /moved/recipes/main/recipe.json
python /path/to/ui-atlas/scripts/atlas.py build /moved/run/atlas.json \
  --source-root /moved/app --recipe /moved/recipes/main/recipe.json \
  --out /moved/run/relocated.html
```

Overrides verify the **original recorded hashes**, including recipe support
files. They do not bless changed bytes. `build` records the checked locators in
the new HTML view without rewriting the original manifest or source evidence.
If bytes differ, the view retains a drift warning; recapture to refresh it.
