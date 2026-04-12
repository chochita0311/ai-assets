# Checklist

Use this as the final quick validator after a document-shaping pass.

## Final Validation
- Was restructuring actually necessary?
- If no meaningful improvement was available, was the document left unchanged?
- Were stable sections left untouched unless there was a clear reason to change them?
- If the input was a document set, were changed files and unchanged stable files reported explicitly?
- If `intake` mode was used, was one primary shaped artifact identified explicitly?
- If `intake` mode emitted derived views, was the primary shaped artifact retained by default?
- Was the minimum effective restructuring applied?
- Is the new structure easier to follow than the original?
- Do headings now match the content they own?
- Are repeated ideas consolidated into one canonical place where appropriate?
- Were rules, caveats, and exceptions preserved?
- Were force words such as `must`, `should`, `only`, `never`, and `unless` preserved accurately?
- Were examples kept near the rules or concepts they qualify?
- Did the pass avoid aesthetic-only rewrites?
- Did the pass avoid introducing artificial structure where the existing structure was already sufficient?
- Did the pass avoid conflicting with established document conventions unless necessary?
- If the input was a related document set, did the pass keep heading patterns reasonably compatible unless divergence clearly helped?
- Does the document now read more seamlessly from section to section?
- Does the structure feel deliberate rather than historically accumulated?
- If the score was used, was it used descriptively instead of as a reason to over-edit?
- Were unchanged stable areas reported explicitly?
- Were low-confidence compressions, merges, or splits avoided or called out?
- If `intake` mode was used, were unresolved or low-confidence fragments handled explicitly?
- If `intake` mode emitted multiple outputs, were derived views labeled explicitly and kept role-distinct?
- If `intake` mode emitted derived views, were they user-requested, user-confirmed, or otherwise clearly justified instead of being treated as an automatic default?
- If `intake` mode did not emit derived views, were any useful next derived views suggested explicitly instead of being silently folded into the current pass?
- If the output was written as a comparison copy, were source-relative terms preserved unless relocation was explicitly requested?
- If the input was PDF or mixed-media, were evidence artifacts and extraction-quality confidence reported when they mattered to trust in the result?
- Did `intake` avoid drifting into PRD, execution planning, repo/docs structure design, or implementation-spec authoring unless explicitly requested?
- If the real issue turned out to be ownership across files, was that boundary called out clearly and, if relevant, was `docs-structuring` suggested as a better fit?

## Final Question
- If this skill runs again on a similar document, is the same composition cleanup unlikely to be needed again without new content drift?
