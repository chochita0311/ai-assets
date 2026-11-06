# Fieldbook list options

The current review is about the note list. These are proposals, not a record of changes already made.

## Reviewed source snapshot

- `notebook.html`: `522572e7cb1f0c41f741113ae67609f27840aeb599f1c95c96788e87a306e5d4`
- `notebook.css`: `f816927b912f54ed2771e9ea33aca9adc710cc8d1c20ac83959a71d97b28ab49`
- `notebook.js`: `8d0d7d87d6eef390f1f45a2ca048c2e745e584dcca4a152f867b976147ff66aa`

## R1 — Scanning rows

Target: `#note-list` and its note entries. Replace the two-column card grid with one compact, full-width sequence of rows. Give each title the strongest local emphasis; remove the repeated sparkle and “A spark worth keeping” line. Keep the excerpt, category, all tags, edited date, any review due date, and full note disclosure with the matching note. Make category and tag meanings distinguishable. Leave the controls and other page regions in place.

## R2 — Category lanes

Target: the same `#note-list` region. Arrange notes into three separately headed category groups instead of one mixed sequence, with compact cards within each group. Retain topic tags, dates, excerpts, and disclosures. Respect the chosen order within each group and retain filtering. This would change the scanning model from one mixed list to grouped lanes.

R1 and R2 are alternatives for the same main presentation. They cannot both be the sole layout of this region. There is no approved mode switch or combined design.

## R3 — Reading plan cleanup

Target: `#reading-board`, outside the note list. Remove its decorative eyebrow and reduce the outer card emphasis while retaining the reading checks, progress, and category/tag explanation.

R3 is independently selectable. None of the proposals calls for changing the hero, navigation, shared tokens, other product pages, or record content.
