const notes = [
  { id: "n1", title: "Interview guide for first-time editors", category: "Research", tags: ["interviews", "writing"], updated: "2026-05-08", review: "2026-05-15", excerpt: "Where new editors hesitate, and what we need to ask next.", body: "Ask people to narrate how they find a draft, check its owner, and decide whether it is ready to share. Avoid suggesting the answer in the question." },
  { id: "n2", title: "Keep status words visible", category: "Decision", tags: ["accessibility", "release"], updated: "2026-05-07", review: null, excerpt: "Color helps scanning; the status word carries the meaning.", body: "Use a written status beside any color cue. This applies to the queue, its filters, and the confirmation after a status change." },
  { id: "n3", title: "Release checklist draft", category: "Draft", tags: ["release", "writing"], updated: "2026-05-06", review: "2026-05-12", excerpt: "A short handoff that names the owner and the remaining evidence.", body: "Record what changed, who checked it, and what remains uncertain. Link the supporting evidence beside the claim it supports." },
  { id: "n4", title: "Keyboard navigation observations", category: "Research", tags: ["accessibility", "interviews"], updated: "2026-05-05", review: null, excerpt: "Two readers lost their place when a panel opened.", body: "One participant returned to the top of the page after closing details. Another could not tell which note was expanded. Check focus position and the expanded state together." },
  { id: "n5", title: "One owner per release item", category: "Decision", tags: ["release"], updated: "2026-05-04", review: null, excerpt: "The person doing the next action is the visible owner.", body: "Contributors remain in the record, but the list shows the one person responsible for the next action. Ownership can change during a handoff." },
  { id: "n6", title: "Plain-language empty states", category: "Draft", tags: ["writing", "accessibility"], updated: "2026-05-03", review: "2026-05-14", excerpt: "Say what happened and give one useful way forward.", body: "When a search has no matches, retain the current filters and explain how to broaden the search. Do not pretend that the underlying notebook is empty." },
  { id: "n7", title: "Interview synthesis — second round", category: "Research", tags: ["interviews"], updated: "2026-05-02", review: null, excerpt: "Most participants began with a topic, then narrowed by note type.", body: "Topic tags crossed Research, Decision, and Draft categories. Participants used the category when they needed the kind of evidence, not just its subject." },
  { id: "n8", title: "Release note opening paragraph", category: "Draft", tags: ["release", "writing"], updated: "2026-05-01", review: null, excerpt: "Lead with what people can now do.", body: "Describe the changed behavior before the implementation detail. Include a limit when it changes how someone should use the feature." }
];

const filters = document.querySelector("#note-filters");
const list = document.querySelector("#note-list");
function renderNotes() {
  const query = document.querySelector("#note-search").value.toLowerCase().trim();
  const category = document.querySelector("#note-category").value;
  const tag = document.querySelector("#note-tag").value;
  const order = document.querySelector("#note-order").value;
  const matches = notes.filter(note => (!query || `${note.title} ${note.excerpt} ${note.body}`.toLowerCase().includes(query)) && (!category || note.category === category) && (!tag || note.tags.includes(tag)));
  matches.sort(order === "title" ? (a, b) => a.title.localeCompare(b.title) : (a, b) => b.updated.localeCompare(a.updated));
  list.replaceChildren();
  for (const note of matches) {
    const article = document.createElement("article");
    article.className = "note-card surface";
    article.id = note.id;
    // All strings below are fixed synthetic fixture data, never user input.
    article.innerHTML = `<div class="note-topline"><span class="note-symbol" aria-hidden="true">✦</span><span class="note-kicker">A spark worth keeping</span></div><h3>${note.title}</h3><p class="note-excerpt">${note.excerpt}</p><div class="note-meta"><span class="category-label">${note.category}</span>${note.tags.map(tag => `<span class="tag-label">#${tag}</span>`).join("")}</div><p class="note-date">Edited <time datetime="${note.updated}">${note.updated}</time></p>${note.review ? `<p class="review-due">Review due <time datetime="${note.review}">${note.review}</time></p>` : ""}<details><summary>Read note</summary><p>${note.body}</p></details>`;
    list.append(article);
  }
  document.querySelector("#note-count").textContent = `${matches.length} of ${notes.length} notes`;
  document.querySelector("#note-empty").hidden = matches.length > 0;
}
filters.addEventListener("submit", event => event.preventDefault());
filters.addEventListener("input", renderNotes);
filters.addEventListener("reset", () => requestAnimationFrame(renderNotes));
document.querySelector("#reading-board").addEventListener("change", () => {
  const checked = document.querySelectorAll('#reading-board input:checked').length;
  document.querySelector("#reading-progress").textContent = `${checked} of 3 read`;
});
renderNotes();
