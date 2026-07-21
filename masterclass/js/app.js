// ============================================================
// App logic: navigation, quiz grading, module gating, progress.
// Progress persists in localStorage so you can leave and return.
// ============================================================

const STORAGE_KEY = "neocloud-masterclass-v1";

const state = loadState();

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch (e) { /* fresh start */ }
  return {
    started: false,
    completedModules: [],   // module ids that passed their quiz
    bestScores: {},         // module id -> best score
    view: { type: "welcome" }
  };
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function isUnlocked(idx) {
  if (idx === 0) return true;
  return state.completedModules.includes(COURSE.modules[idx - 1].id);
}

function isDone(id) {
  return state.completedModules.includes(id);
}

// ---------- Rendering ----------

const sidebarEl = document.getElementById("sidebar-nav");
const mainEl = document.getElementById("main");
const progressFill = document.getElementById("progress-fill");
const progressText = document.getElementById("progress-text");

function render() {
  renderSidebar();
  const v = state.view;
  if (v.type === "welcome") renderWelcome();
  else if (v.type === "module") renderModule(v.moduleIdx, v.tab);
  else if (v.type === "done") renderCertificate();
  saveState();
  window.scrollTo({ top: 0 });
}

function renderSidebar() {
  const done = state.completedModules.length;
  const total = COURSE.modules.length;
  progressFill.style.width = `${(done / total) * 100}%`;
  progressText.textContent = `${done} / ${total} modules passed`;

  sidebarEl.innerHTML = "";
  COURSE.modules.forEach((m, idx) => {
    const unlocked = isUnlocked(idx);
    const btn = document.createElement("button");
    btn.className = "nav-module"
      + (isDone(m.id) ? " done" : "")
      + (!unlocked ? " locked" : "")
      + (state.view.type === "module" && state.view.moduleIdx === idx ? " active" : "");
    btn.innerHTML = `
      <span class="badge">${isDone(m.id) ? "✓" : (unlocked ? m.number : "🔒")}</span>
      <span class="meta">
        <span class="t">Module ${m.number}: ${m.title}</span>
        <span class="s">${m.subtitle}</span>
      </span>`;
    if (unlocked) {
      btn.onclick = () => { state.view = { type: "module", moduleIdx: idx, tab: 0 }; render(); };
    }
    sidebarEl.appendChild(btn);
  });
}

function renderWelcome() {
  mainEl.innerHTML = `
  <div class="welcome">
    <div class="hero">
      <div class="kicker">A 5-Module Interactive Course</div>
      <h2>${COURSE.title}</h2>
      <p>${COURSE.tagline}</p>
      <p style="margin-top:12px">Built for an entrepreneur with no IT background. Every concept comes with the business reason behind it, the EdgeUno case woven throughout, and a gated knowledge check before you advance.</p>
      <button class="btn" id="start-btn">${state.started ? "Continue the course →" : "Start Module 1 →"}</button>
    </div>
    <div class="how-cards">
      <div class="how-card"><div class="ico">📖</div><h4>Short lessons</h4><p>Each module has 3 bite-size lessons (~4 min each). Read them in order using the tabs at the top.</p></div>
      <div class="how-card"><div class="ico">💰</div><h4>The "Why" callouts</h4><p>Gold boxes follow the money. Blue boxes apply the EdgeUno case. Purple boxes are your entrepreneur playbook.</p></div>
      <div class="how-card"><div class="ico">🔒</div><h4>Gated quizzes</h4><p>5 challenging questions per module. Score ${COURSE.passScore}/5 to unlock the next module — wrong answers come with explanations so you learn from misses.</p></div>
      <div class="how-card"><div class="ico">💾</div><h4>Progress saved</h4><p>Your progress is stored in this browser. Close the tab and come back anytime — you'll resume where you left off.</p></div>
    </div>
  </div>`;
  document.getElementById("start-btn").onclick = () => {
    state.started = true;
    // resume at first incomplete module
    let idx = COURSE.modules.findIndex(m => !isDone(m.id));
    if (idx === -1) { state.view = { type: "done" }; }
    else state.view = { type: "module", moduleIdx: idx, tab: 0 };
    render();
  };
}

function renderModule(idx, tab) {
  const m = COURSE.modules[idx];
  const lessonCount = m.lessons.length;
  const isQuizTab = tab === lessonCount;

  const tabsHtml = m.lessons.map((l, i) =>
    `<button class="${i === tab ? "active" : ""}" data-tab="${i}">Lesson ${m.number}.${i + 1}</button>`
  ).join("") +
  `<button class="quiz-tab ${isQuizTab ? "active" : ""}" data-tab="${lessonCount}">🎯 Knowledge Check</button>`;

  let bodyHtml;
  if (!isQuizTab) {
    const lesson = m.lessons[tab];
    const isLastLesson = tab === lessonCount - 1;
    bodyHtml = `
      <div class="lesson">
        <h3>${lesson.title}</h3>
        ${lesson.body}
      </div>
      <div class="lesson-nav">
        ${tab > 0
          ? `<button class="btn ghost" id="prev-btn">← Previous lesson</button>`
          : `<span></span>`}
        <button class="btn ${isLastLesson ? "gold" : ""}" id="next-btn">
          ${isLastLesson ? "Take the Knowledge Check →" : "Next lesson →"}
        </button>
      </div>`;
  } else {
    bodyHtml = renderQuizHtml(m);
  }

  mainEl.innerHTML = `
    <div class="module-header">
      <div class="kicker">Module ${m.number} of ${COURSE.modules.length}</div>
      <h2>${m.title}</h2>
      <p class="subtitle">${m.subtitle}</p>
    </div>
    <div class="lesson-tabs">${tabsHtml}</div>
    <div id="module-body">${bodyHtml}</div>`;

  mainEl.querySelectorAll(".lesson-tabs button").forEach(b => {
    b.onclick = () => { state.view.tab = parseInt(b.dataset.tab, 10); render(); };
  });
  const prev = document.getElementById("prev-btn");
  if (prev) prev.onclick = () => { state.view.tab = tab - 1; render(); };
  const next = document.getElementById("next-btn");
  if (next) next.onclick = () => { state.view.tab = tab + 1; render(); };

  if (isQuizTab) wireQuiz(m, idx);
}

// ---------- Quiz ----------

let quizSelections = {};

function renderQuizHtml(m) {
  quizSelections = {};
  const best = state.bestScores[m.id];
  const passed = isDone(m.id);
  const qHtml = m.quiz.map((q, qi) => `
    <div class="qcard" data-q="${qi}">
      <div class="qnum">Question ${qi + 1} of ${m.quiz.length}</div>
      <div class="qtext">${q.q}</div>
      ${q.options.map((o, oi) => `
        <button class="opt" data-q="${qi}" data-o="${oi}">
          <span class="letter">${"ABCD"[oi]}</span><span>${o}</span>
        </button>`).join("")}
      <div class="explain-slot"></div>
    </div>`).join("");

  return `
    <div class="quiz-intro">
      <strong>Knowledge Check — Module ${m.number}.</strong>
      Answer all ${m.quiz.length} questions, then grade yourself. You need <strong>${COURSE.passScore}/${m.quiz.length}</strong> to unlock the next module.
      ${passed ? ` You've already passed this one (best: ${best}/${m.quiz.length}) — retake it anytime.` : (best !== undefined ? ` Best attempt so far: ${best}/${m.quiz.length}.` : "")}
    </div>
    ${qHtml}
    <div class="quiz-actions">
      <button class="btn gold" id="grade-btn" disabled>Grade my answers</button>
      <span style="color:var(--text-dim);font-size:13.5px" id="answered-count">0 of ${m.quiz.length} answered</span>
    </div>
    <div id="result-slot"></div>`;
}

function wireQuiz(m, moduleIdx) {
  const gradeBtn = document.getElementById("grade-btn");
  const countEl = document.getElementById("answered-count");

  mainEl.querySelectorAll(".opt").forEach(btn => {
    btn.onclick = () => {
      if (btn.classList.contains("disabled")) return;
      const qi = btn.dataset.q, oi = parseInt(btn.dataset.o, 10);
      quizSelections[qi] = oi;
      mainEl.querySelectorAll(`.opt[data-q="${qi}"]`).forEach(b => b.classList.remove("selected"));
      btn.classList.add("selected");
      const answered = Object.keys(quizSelections).length;
      countEl.textContent = `${answered} of ${m.quiz.length} answered`;
      gradeBtn.disabled = answered < m.quiz.length;
    };
  });

  gradeBtn.onclick = () => {
    let score = 0;
    m.quiz.forEach((q, qi) => {
      const chosen = quizSelections[qi];
      const card = mainEl.querySelector(`.qcard[data-q="${qi}"]`);
      card.querySelectorAll(".opt").forEach(b => {
        const oi = parseInt(b.dataset.o, 10);
        b.classList.add("disabled");
        if (oi === q.answer) b.classList.add("correct");
        else if (oi === chosen) b.classList.add("wrong");
      });
      const good = chosen === q.answer;
      if (good) score++;
      card.querySelector(".explain-slot").innerHTML =
        `<div class="explain"><strong>${good ? "Correct." : "Not quite."}</strong> ${q.explain}</div>`;
    });

    state.bestScores[m.id] = Math.max(state.bestScores[m.id] || 0, score);
    const passed = score >= COURSE.passScore;
    if (passed && !isDone(m.id)) state.completedModules.push(m.id);
    saveState();
    renderSidebar();

    const isLast = moduleIdx === COURSE.modules.length - 1;
    const resultSlot = document.getElementById("result-slot");
    if (passed) {
      resultSlot.innerHTML = `
        <div class="result-banner pass">
          <h3>✅ Passed — ${score}/${m.quiz.length}</h3>
          <p>You've demonstrated a firm grasp of Module ${m.number}. ${isLast ? "That was the final module." : "The next module is now unlocked."}</p>
          <button class="btn" id="advance-btn">${isLast ? "Finish the course 🎓" : `Continue to Module ${m.number + 1} →`}</button>
        </div>`;
      document.getElementById("advance-btn").onclick = () => {
        state.view = isLast ? { type: "done" } : { type: "module", moduleIdx: moduleIdx + 1, tab: 0 };
        render();
      };
    } else {
      resultSlot.innerHTML = `
        <div class="result-banner fail">
          <h3>Not yet — ${score}/${m.quiz.length}</h3>
          <p>You need ${COURSE.passScore}/${m.quiz.length} to advance. Read the explanations above — they show exactly where your knowledge is lagging — then review the lessons and retake the check.</p>
          <button class="btn ghost" id="review-btn" style="margin-right:10px">Review lessons</button>
          <button class="btn gold" id="retake-btn">Retake the check</button>
        </div>`;
      document.getElementById("review-btn").onclick = () => { state.view.tab = 0; render(); };
      document.getElementById("retake-btn").onclick = () => render();
    }
    resultSlot.scrollIntoView({ behavior: "smooth", block: "center" });
  };
}

function renderCertificate() {
  mainEl.innerHTML = `
    <div class="certificate">
      <div class="ico">🎓</div>
      <h2>Masterclass Complete</h2>
      <p>You passed all five knowledge checks. You can now explain how AS 7195 became a giant without owning pipes, price a wavelength, decide when asset-light should flip to asset-owner, and — most importantly — run any Latin American infrastructure idea through the Opportunity Filter.</p>
      <p style="margin-top:14px"><strong style="color:var(--gold)">Your assignment:</strong> pick one country and one customer segment you already know, run the five filter questions from Lesson 5.3, and write a one-page memo naming the buyer, the gap the giants can't serve, and what you'll own when it works.</p>
      <button class="btn" style="margin-top:22px" id="revisit-btn">Revisit any module</button>
    </div>`;
  document.getElementById("revisit-btn").onclick = () => {
    state.view = { type: "module", moduleIdx: 0, tab: 0 };
    render();
  };
}

// ---------- Reset ----------
document.getElementById("reset-btn").onclick = () => {
  if (confirm("Reset all course progress? Your quiz scores and unlocked modules will be cleared.")) {
    localStorage.removeItem(STORAGE_KEY);
    location.reload();
  }
};

render();
