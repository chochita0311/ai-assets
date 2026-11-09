# Menu topics and recorded state links

## Contents

- [Product map](#product-map)
- [Workspace configuration](#workspace-configuration)
- [Composition and evidence](#composition-and-evidence)
- [Action links](#action-links)
- [Opinions and compatibility](#opinions-and-compatibility)
- [Verification](#verification)

## Product map

Derive the entry, menu order, topic boundaries and feature names from the actual
product. A capture batch is an execution concern; it need not be a visible topic.
Keep an ordinary feature state with its relevant dropdowns, dialogs, loading,
empty, error, cancellation and recovery branches. Avoid an unrelated top-level
"errors" or "overlays" collection that users must search to finish one feature.

Use separate product groups for real edition/scope differences. Within a topic,
use feature regions and original journey branches. Broad and narrow viewports
are variants of these states. Do not manufacture all combinations, claim every
control is covered, or hide unobserved states behind a successful batch count.

## Workspace configuration

Author `<workspace>/navigation.json` as private, app-owned atlas input. Its
`ui-atlas.navigation/v1` schema has an ordered `topics` array. Each topic has a
stable `id`, readable `label`, product `group`, optional `description`, and ordered
`features`. Each feature has a stable `id`, `label`, and `select` entries:

```json
{
  "schema": "ui-atlas.navigation/v1",
  "topics": [{
    "id": "settings", "label": "Settings", "group": "App",
    "features": [{
      "id": "profiles", "label": "Profiles",
      "select": [
        {"atlas": "app-basics", "frames": ["profiles.*"], "flow_label": "List"},
        {"atlas": "app-disclosures", "frames": ["profile-menu.*"], "flow_label": "Color menu"}
      ],
      "missing": [{"label": "Native chooser", "reason": "Host was not exercised"}]
    }]
  }]
}
```

`atlas` identifies an original observation atlas. `frames` contains shell-style
patterns over its stable state IDs, resolved against its latest readable run.
Each selection must match at least one state. Optional `labels` maps original
state IDs to shorter presentation labels; `flow_label` names a journey branch.
`variant` can be `wide` or `narrow`; otherwise the observed viewport supplies it.
Keep a presentation label distinct from evidence of what the app displays.

Each original atlas/state pair has one primary topic/feature. Duplicate ownership,
unknown observations and unmatched selections stop the build. Unassigned states
are listed in the menu map and remain accessible in original captures. Treat an
unexpected unassigned state as an organization gap, not silent deletion.

Run `python scripts/atlas.py catalog <workspace>` after writing the map or adding
observations. It builds `topics/<topic-id>.html` and updates the workspace entry.
Without `navigation.json`, ordinary sheet hosting is unchanged. Keep authored
configuration and reusable capture recipes; topic HTML is a rebuildable view.

## Composition and evidence

The composer uses the existing inert-DOM builder for every original observation.
It preserves each recorded document, state ID, identity, condition, payload,
source/recipe hashes, staleness qualification and replay command under its origin.
The derived payload uses `ui-atlas.topic/v1`; original observation manifests
retain `ui-atlas/v2`. Qualified view IDs distinguish equal state IDs in different
source atlases. Payload also identifies its original state, observation identity,
source revision and recipe hash, with a link to the complete original manifest.
Composition does not rewrite manifests, move source frames or recapture the app.

Topic layout groups features and keeps original journeys separate within them.
Canvas links identify observed transitions; rows alone do not assert temporal
order between independent journeys. Viewport filtering never substitutes a
different observation for a missing variant. A note or search result can reveal
the variant containing its actual target.

The entry remembers the topic. Product-group/topic selection and the complete
menu map replace flat capture-batch navigation. Fully mapped latest captures are
backing inputs and do not repeat as menu entries. Unassigned captures and retained
earlier runs remain under a disclosure; omit it when neither exists. Payload
retains access to its required source manifest. Old `#atlas=` links resolve to the
owning topic; explicit `#run=` links open that run while retained. A missing
explicit run reports its absence instead of silently opening a different
observation. Unsaved drafts and pending
note operations retain their existing owner and close/reload guards while topics
change. Reorganization does not itself authorize pruning observations or resetting
feedback. For requested cleanup, follow
[run retention and dependency checks](artifact-workspace.md#retain-move-and-clean-up).

## Action links

The capture runner records transitions between consecutive checkpoints in one
journey. A trigger selector is resolved in the actual source DOM before its
action. Compound gestures and response-only changes stay frame-level links
instead of implying that one control performs the whole sequence. This ties inspection of the recorded control to the following observed
state. Read-only response releases and other non-control steps remain in Payload.

Older captures can infer checkpoint links from a shared recorded step prefix;
these remain frame-level when the trigger cannot be identified reliably. To join
separately captured but verified related states, author a topic `links` entry:

```json
{
  "from": ["app-basics", "profiles.wide"],
  "to": ["app-disclosures", "profile-menu.open.wide"],
  "label": "Open color menu",
  "element_selector": "#profile-color"
}
```

Both endpoints must belong to that topic. A failed or unobserved endpoint stays
a qualified gap; do not infer its trigger or focus, and keep other observations
available. For rendered endpoints, `element_selector` must exactly match
one visible inventory selector; alternatively use a uniquely matched
`element_label`. Missing or ambiguous triggers stop the build. Optional `focus_selector` identifies
exactly one visible element in the result, such as the opened popover. It focuses
that observed result while retaining its whole-screen canvas context; missing or
ambiguous result focus also stops the build. Omit a trigger
only for a frame-level reference; do not make it a positional substitute for a
specific control. Author cross-capture links only when source/context evidence
supports the relationship, and exercise the corresponding actual replay.

Element inspection remains the default. The inspector lists related recorded
states. In "follow states" mode, a uniquely linked trigger jumps to its recorded
result; multiple branches require a choice, and absent links are reported.
Neither mode operates the original app, navigates its external links, saves
settings or makes app network requests. Use actual replay for live interaction.

## Opinions and compatibility

Topic feedback reads/writes the original atlas namespace and original state ID.
It projects view IDs without migrating, deleting or rewriting stored opinions.
Old identities, quotes, clipping qualifications, kind and review status survive.
Unknown old frames remain qualified missing-frame opinions; known states owned
by another topic remain scoped to that topic.

Topic export uses `ui-atlas.notes/v2`: `sources` contains original
`ui-atlas.notes/v1` envelopes. Topic import accepts a source v1 envelope or its v2
bundle and preserves explicit conflict choices, pending-write recovery and
concurrent-change checks. An original standalone viewer rebuilt with this version accepts its matching
source from a v2 bundle; other sources remain in the file. A topic refuses a
bundle containing unknown source owners instead of silently dropping them.

Local-file storage remains browser-dependent. When a browser isolates different
file URLs, export opinions from original viewers and import them into the topic;
keep the exports as backups. Composition cannot bypass browser storage isolation.

## Verification

Compare topic membership with the original state inventory, including failed,
unverified and not-applicable states. Follow a menu into ordinary, disclosure and
exception states without choosing an execution batch. Inspect named elements and
Payload, then exercise trigger/result links, branch choices and missing links.
Check original manifests/identities and old opinion keys before and after.

Exercise wide/narrow filtering, cross-topic drafts, pending saves/deletions,
conflicting import, other-tab changes, old links, history, fit/pan/zoom and narrow
inspector access. Verify popover geometry and selectable children against the
actual renderer. Rebuilding or composing an atlas does not run that renderer;
report resource checks and actual app replay as separate evidence.
