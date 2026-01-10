let currentCard = null;
let seenThisSession = 0;
let score = 0;

function $(id) { return document.getElementById(id); }
function setHidden(id, hidden) { $(id).classList.toggle("hidden", hidden); }

async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || `Request failed: ${res.status}`);
  return data;
}

function resetPanels() {
  // Learn
  $("translation").textContent = "";
  setHidden("translation", true);
  setHidden("nextLearn", true);
  setHidden("reveal", false);
  $("metaLearn").textContent = "";

  // Test
  $("answer").value = "";
  $("feedback").textContent = "";
  setHidden("nextTest", true);
  $("metaTest").textContent = "";
}

function updateModeUI() {
  const mode = $("mode").value;
  setHidden("learnPanel", mode !== "learn");
  setHidden("testPanel", mode !== "test");

  // Score only shown in test mode
  setHidden("scoreRow", mode !== "test");
}

async function loadCategories() {
  const data = await fetchJSON("/api/categories");
  const select = $("category");
  select.innerHTML = "";

  for (const cat of data.categories) {
    const opt = document.createElement("option");
    opt.value = cat;
    opt.textContent = cat;
    select.appendChild(opt);
  }
  if (data.categories.length > 0) select.value = data.categories[0];
}

async function refreshStats() {
  const category = $("category").value;
  const stats = await fetchJSON(`/api/stats?category=${encodeURIComponent(category)}`);

  $("seenSession").textContent = String(seenThisSession);
  $("seenUnique").textContent = String(stats.unique_seen_in_category);
  $("totalCat").textContent = String(stats.total_in_category);
  $("score").textContent = String(score);
}

async function loadNext() {
  const category = $("category").value;
  const data = await fetchJSON(`/api/next?category=${encodeURIComponent(category)}`);

  currentCard = data;
  $("prompt").textContent = data.lt;

  const pron = (data.pronunciation || "").trim();
  $("pronunciation").textContent = pron ? `Pronunciation: ${pron}` : "";

  resetPanels();

  // Meta
  $("metaLearn").textContent = `Seen count (this card): ${data.seen_count}`;
  $("metaTest").textContent = `Seen count (this card): ${data.seen_count}`;

  await refreshStats();

  // Focus input in test mode
  if ($("mode").value === "test") $("answer").focus();
}

async function markSeen() {
  if (!currentCard) return;
  await fetchJSON("/api/seen", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ card_id: currentCard.id }),
  });
  seenThisSession += 1;
}

async function revealLearn() {
  await markSeen();
  $("translation").textContent = currentCard.en;
  setHidden("translation", false);
  setHidden("nextLearn", false);
  setHidden("reveal", true);

  currentCard.seen_count += 1;
  $("metaLearn").textContent = `Seen count (this card): ${currentCard.seen_count}`;

  await refreshStats();
}

async function submitTest() {
  if (!currentCard) return;

  const answer = $("answer").value;

  const result = await fetchJSON("/api/check", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ card_id: currentCard.id, answer }),
  });

  // Mark as seen when they attempt (so progress moves in Test mode too)
  await markSeen();

  if (result.is_correct) {
    score += 1;
    $("feedback").textContent = "✅ Correct!";
  } else {
    $("feedback").textContent = `❌ Nope. Answer: ${result.correct_answer}`;
  }

  setHidden("nextTest", false);
  currentCard.seen_count += 1;
  $("metaTest").textContent = `Seen count (this card): ${currentCard.seen_count}`;

  await refreshStats();
}

$("reveal").addEventListener("click", () => revealLearn().catch(e => alert(e.message)));
$("nextLearn").addEventListener("click", () => loadNext().catch(e => alert(e.message)));

$("submit").addEventListener("click", () => submitTest().catch(e => alert(e.message)));
$("answer").addEventListener("keydown", (e) => {
  if (e.key === "Enter") submitTest().catch(err => alert(err.message));
});
$("nextTest").addEventListener("click", () => loadNext().catch(e => alert(e.message)));

$("mode").addEventListener("change", () => {
  updateModeUI();
  // Reset score only when switching into test? (keeps it strict)
  if ($("mode").value === "test") score = 0;
  refreshStats().catch(() => {});
  if ($("mode").value === "test") $("answer").focus();
});

$("category").addEventListener("change", () => {
  // Reset session counter when category changes
  seenThisSession = 0;
  // Reset score if in test mode
  if ($("mode").value === "test") score = 0;
  loadNext().catch(e => alert(e.message));
});

(async function boot() {
  try {
    updateModeUI();
    await loadCategories();
    await loadNext();
  } catch (e) {
    $("prompt").textContent = e.message;
  }
})();
