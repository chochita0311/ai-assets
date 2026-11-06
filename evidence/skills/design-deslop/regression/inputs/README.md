# Local product prototypes

Open `notebook.html`, `galaxy.html`, or `queue.html` in a browser. For a local server, run `python3 -m http.server 8000` from this directory, then open the chosen page at `http://localhost:8000/`.

- **Fieldbook:** eight searchable notes with distinct category and tag filters, sorting, review deadlines, disclosures, and a separate reading checklist.
- **Nightfold:** four fictional sky entries with search, type filtering, save toggles, a saved-only view, and a separate club bulletin month selector.
- **Release desk:** five review items with title/owner search, status and assignee filters, and review-note disclosures.

There is no package installation, build step, external network request, or backend. The pages use fixed synthetic data. `DESIGN.md` records fixed decisions and areas open to visual changes. Page state resets on reload.
