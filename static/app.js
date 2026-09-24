const form = document.querySelector("#analysis-form");
const requirements = document.querySelector("#requirements");
const template = document.querySelector("#requirement-template");
const emptyState = document.querySelector("#empty-state");
const results = document.querySelector("#results");
const submitButton = document.querySelector("#submit-button");

const lines = value => value.split("\n").map(v => v.trim()).filter(Boolean);
const esc = value => String(value ?? "").replace(/[&<>'"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"}[c]));

function renumberRequirements() {
  const cards = [...requirements.querySelectorAll(".requirement-card")];
  cards.forEach((card, index) => card.querySelector("h3").textContent = `Wymaganie ${index + 1}`);
  emptyState.hidden = cards.length > 0;
}

function addRequirement() {
  const node = template.content.cloneNode(true);
  node.querySelector(".remove").addEventListener("click", event => {
    event.target.closest(".requirement-card").remove();
    renumberRequirements();
  });
  requirements.appendChild(node);
  renumberRequirements();
}

function getRequirements() {
  return [...requirements.querySelectorAll(".requirement-card")].map((card, index) => {
    const value = name => card.querySelector(`[data-field="${name}"]`).value.trim();
    return {
      id: value("id") || `BR-DRAFT-${String(index + 1).padStart(3,"0")}`,
      type: value("type"),
      statement: value("statement"),
      rationale: value("rationale") || null,
      owner: value("owner") || null,
      source_refs: lines(value("source_refs")),
      acceptance_criteria: [], dependencies: [], status: "draft", version: 1
    };
  }).filter(item => item.statement);
}

function renderRun(run) {
  const statusLabels = {completed:"ukończony",needs_input:"wymaga informacji",stubbed:"zaślepiony",needs_approval:"wymaga akceptacji",failed:"błąd"};
  document.querySelector("#run-summary").textContent = `Status: ${statusLabels[run.status] || run.status}. ID analizy: ${run.id}`;
  document.querySelector("#steps").innerHTML = run.steps.map(step => {
    const questions = step.questions?.length ? `<p><strong>Pytania i następne działania</strong></p><ul>${step.questions.map(q => `<li>${esc(q)}</li>`).join("")}</ul>` : "";
    const findings = step.findings?.length ? `<p><strong>Ustalenia</strong></p><ul>${step.findings.map(f => `<li class="finding-${esc(f.severity)}"><strong>${esc(f.rule_id)}</strong>${f.artifact_id ? ` · ${esc(f.artifact_id)}` : ""}: ${esc(f.message)}</li>`).join("")}</ul>` : "";
    const gate = step.approval_gate ? `<p><strong>Akceptacja:</strong> ${esc(step.approval_gate.replaceAll("_"," "))}</p>` : "";
    const checked = step.outputs?.checked !== undefined ? `<p><strong>Sprawdzono wymagań:</strong> ${esc(step.outputs.checked)}</p>` : "";
    return `<article class="step"><div class="step-head"><h3>${esc(step.skill)}</h3><span class="status status-${esc(step.status)}">${esc(statusLabels[step.status] || step.status)}</span></div><div class="step-body">${checked}${gate}${questions}${findings || (!questions ? "<p>Brak dodatkowych uwag.</p>" : "")}</div></article>`;
  }).join("");
  results.hidden = false;
  results.scrollIntoView({behavior:"smooth", block:"start"});
}

document.querySelector("#add-requirement").addEventListener("click", addRequirement);
form.addEventListener("reset", () => setTimeout(() => { requirements.innerHTML = ""; renumberRequirements(); results.hidden = true; }, 0));
form.addEventListener("submit", async event => {
  event.preventDefault();
  submitButton.disabled = true;
  submitButton.textContent = "Analizuję…";
  results.hidden = true;
  const payload = {
    pipeline: document.querySelector("#pipeline").value,
    initiative: {
      title: document.querySelector("#title").value.trim(),
      problem: document.querySelector("#problem").value.trim(),
      desired_outcome: document.querySelector("#outcome").value.trim(),
      sources: lines(document.querySelector("#sources").value),
      stakeholders: lines(document.querySelector("#stakeholders").value),
      constraints: lines(document.querySelector("#constraints").value)
    },
    requirements: getRequirements()
  };
  try {
    const response = await fetch("/v1/runs", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(payload)});
    if (!response.ok) throw new Error((await response.json()).detail || "Nie udało się uruchomić analizy.");
    renderRun(await response.json());
  } catch (error) {
    results.hidden = false;
    document.querySelector("#run-summary").textContent = "Analiza nie została uruchomiona.";
    document.querySelector("#steps").innerHTML = `<div class="error-box">${esc(error.message)}</div>`;
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Uruchom analizę";
  }
});

renumberRequirements();
