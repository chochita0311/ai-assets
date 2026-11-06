const skyEntries = [
  { id: "s1", name: "Ribbon cloud", type: "Cloud", window: "20:10–21:00", excerpt: "A rose-colored thread in the club’s imaginary sky.", note: "Mira sketched two folds and left the darker middle untouched. The blank space is part of the drawing." },
  { id: "s2", name: "Blue lantern", type: "Cluster", window: "20:30–22:10", excerpt: "A loose gathering of lights above the painted ridge.", note: "Count the bright points before reading the old sketch. Different observers have given this patch three different names." },
  { id: "s3", name: "Little courier", type: "Satellite", window: "21:05–21:18", excerpt: "One quiet line across a very large page.", note: "The club records a short trail, a start time, and the direction it crossed the page. These are fictional demo observations." },
  { id: "s4", name: "Paper crown", type: "Cluster", window: "21:20–23:00", excerpt: "Five warm points, folded into a familiar shape.", note: "A new member saw a crown; another saw a paper boat. Both descriptions stay in the journal." }
];
const savedEntries = new Set();
function renderSky() {
  const query = document.querySelector("#sky-search").value.toLowerCase().trim();
  const type = document.querySelector("#sky-type").value;
  const savedOnly = document.querySelector("#sky-saved").checked;
  const matches = skyEntries.filter(entry => (!query || `${entry.name} ${entry.excerpt} ${entry.note}`.toLowerCase().includes(query)) && (!type || type === entry.type) && (!savedOnly || savedEntries.has(entry.id)));
  const list = document.querySelector("#sky-list");
  list.replaceChildren();
  for (const entry of matches) {
    const article = document.createElement("article");
    article.className = "sky-card";
    article.id = entry.id;
    article.innerHTML = `<span class="sky-emblem" aria-hidden="true"></span><p class="eyebrow">Discover your next wonder</p><h3>${entry.name}</h3><p>${entry.excerpt}</p><span class="sky-window">Demo window · ${entry.window}</span><div class="sky-actions"><span>${entry.type}</span><button type="button" data-save="${entry.id}" aria-pressed="${savedEntries.has(entry.id)}">${savedEntries.has(entry.id) ? "Saved" : "Save for tonight"}</button></div><details><summary>Read field note</summary><p>${entry.note}</p></details>`;
    list.append(article);
  }
  document.querySelector("#sky-count").textContent = `${matches.length} of ${skyEntries.length} entries`;
  document.querySelector("#saved-count").textContent = `${savedEntries.size} saved for tonight`;
  document.querySelector("#sky-empty").hidden = matches.length > 0;
}
document.querySelector("#sky-filters").addEventListener("submit", event => event.preventDefault());
document.querySelector("#sky-filters").addEventListener("input", renderSky);
document.querySelector("#sky-list").addEventListener("click", event => {
  const button = event.target.closest("button[data-save]");
  if (!button) return;
  const id = button.dataset.save;
  savedEntries.has(id) ? savedEntries.delete(id) : savedEntries.add(id);
  renderSky();
  document.querySelector(`button[data-save="${id}"]`)?.focus();
});
const bulletins = {
  may: [{ title: "Sketch exchange", text: "Bring one page, including the unfinished parts." }, { title: "Quiet hour", text: "The first half-hour is for looking; conversation follows." }],
  april: [{ title: "Paper lantern evening", text: "Members compared three ways to draw a pale glow." }]
};
function renderBulletin() {
  const items = bulletins[document.querySelector("#bulletin-month").value];
  document.querySelector("#bulletin-list").innerHTML = items.map(item => `<article><h3>${item.title}</h3><p>${item.text}</p></article>`).join("");
}
document.querySelector("#bulletin-month").addEventListener("change", renderBulletin);
renderSky();
renderBulletin();
