# Design decisions

These three small local prototypes belong to different products. They share spacing and form primitives for convenience, not one mandatory visual identity. Each page has its own stylesheet and script. Keep an edit to one product from changing another product incidentally.

## Common constraints

- Keep the pages runnable without a build step, network access, external fonts, images, or added dependencies.
- Keep the navigation, labeled controls, keyboard focus visibility, result counts, empty states, and working details disclosures.
- Preserve the supplied sample records. Promotional framing can change; record titles, descriptions, body text, owners, dates, and meanings must survive a visual edit.
- Keep controls usable at both a wide desktop width and a 390-pixel phone width. A deliberately scrollable data table is acceptable on the phone; unintended page-wide horizontal overflow is not.
- State is local to the open page. Reading checks and saved sky entries reset on reload; persistence is outside this prototype’s scope.
- Scope a selected-region change to that region. Shared tokens can affect all three products.

## Fieldbook — notebook.html

The job is finding an existing note, understanding what kind of note it is, and opening its text. The current promotional framing and repeated decorative card chrome are experiments, not brand requirements.

Fixed:

- A note has exactly one **category**: Research, Decision, or Draft. This describes the kind of evidence or writing.
- A note has zero or more **tags**. Tags describe topics across categories. A tag must not be turned into a category, or categories and tags merged into one undifferentiated taxonomy.
- Search matches note title and text. Category and tag filters combine with search. The order control offers recently edited and title order; reset clears every note filter.
- Display the edited date for each note. Current revision also includes an optional **review due date**, which is the next review deadline, not its edited date. It must remain visible on the corresponding note when set.
- Each note’s full body remains available through a working disclosure.
- The reading plan in `#reading-board` is a separate region. Its three checkboxes and progress count must work independently of note filtering.

Open:

- List density, card versus row treatment, useful hierarchy, the amount of promotional copy, borders, shadows, small decorative icons, and label presentation.
- Category and tag styling, provided their different meanings remain legible.

## Nightfold — galaxy.html

Nightfold is an imaginary observing club’s sky journal, not an astronomical guide. Its expressive night-sky direction has already been chosen. The emotional appeal is part of the product.

Fixed:

- Preserve the deep indigo night, star field, intersecting orbit motif, warm pink/peach and cool lavender/cyan light, and a visible sense of glow. Rounded content containers are part of this direction.
- Georgia display type and the system sans-serif body are intentional and avoid a font download. Familiar fonts, glows, gradients, and cards are not defects by themselves.
- Object names, types, fictional time windows, field-note text, search, type filter, save toggles, saved-only filter, and live counts retain their meaning and behavior.
- The club bulletin and its month selector are independent from the evening watch list.

Open:

- How strongly an individual surface glows, local spacing and hierarchy, redundant slogans, repeated ornaments, and which information needs emphasis.
- Simplifying one part does not require every part to have the same visual intensity.

## Release desk — queue.html

The job is choosing the next item to review. The plain table is the current chosen direction; it has no planned rebrand.

Fixed:

- Keep the status words Ready, Needs info, and Scheduled visible. Color only supplements those words.
- Preserve item, owner, due date, and review notes, in due-date order.
- Search matches title or owner; status and assigned-to-me filters combine; clear resets all filters.
- Keep the result count and empty state accurate.

Open:

- Make a local improvement only when it solves an observed problem for this task. Keeping the current screen is a valid outcome.
