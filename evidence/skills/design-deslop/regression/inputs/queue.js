const queueItems = [
  { id: "q1", title: "Clarify the draft handoff", status: "Ready", owner: "Robin", due: "2026-05-09", note: "Compare the new opening paragraph with the approved brief. Text is ready; one reviewer is needed." },
  { id: "q2", title: "Check keyboard focus after closing details", status: "Needs info", owner: "Jules", due: "2026-05-10", note: "The focus trace is missing for the narrow-screen layout. Record it before scheduling release." },
  { id: "q3", title: "Publish the status glossary", status: "Scheduled", owner: "Imani", due: "2026-05-11", note: "Language review is complete. The page is scheduled with the next documentation update." },
  { id: "q4", title: "Review empty search guidance", status: "Ready", owner: "Robin", due: "2026-05-12", note: "Verify that the guidance distinguishes no matches from an empty account." },
  { id: "q5", title: "Resolve the missing owner label", status: "Needs info", owner: "Noor", due: "2026-05-13", note: "Confirm which team owns the next action, then update the item before review." }
];
function renderQueue() {
  const query = document.querySelector("#queue-search").value.toLowerCase().trim();
  const status = document.querySelector("#queue-status").value;
  const mine = document.querySelector("#queue-mine").checked;
  const matches = queueItems.filter(item => (!query || `${item.title} ${item.owner}`.toLowerCase().includes(query)) && (!status || item.status === status) && (!mine || item.owner === "Robin"));
  document.querySelector("#queue-list").innerHTML = matches.map(item => `<tr id="${item.id}"><td><p class="item-title">${item.title}</p><details><summary>Review notes</summary><p>${item.note}</p></details></td><td><span class="status-word status-${item.status.toLowerCase().replaceAll(" ", "-")}">${item.status}</span></td><td>${item.owner}</td><td><time datetime="${item.due}">${item.due}</time></td></tr>`).join("");
  document.querySelector("#queue-count").textContent = `${matches.length} of ${queueItems.length} items`;
  document.querySelector("#queue-empty").hidden = matches.length > 0;
}
document.querySelector("#queue-filters").addEventListener("submit", event => event.preventDefault());
document.querySelector("#queue-filters").addEventListener("input", renderQueue);
document.querySelector("#queue-filters").addEventListener("reset", () => requestAnimationFrame(renderQueue));
renderQueue();
