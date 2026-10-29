"use strict";

const directionSelect = document.querySelector("#direction");
const sourceLanguage = document.querySelector("#source-language");
const targetLanguage = document.querySelector("#target-language");
const sourcePill = document.querySelector("#source-pill");
const targetPill = document.querySelector("#target-pill");
const sourceText = document.querySelector("#source-text");
const characterCount = document.querySelector("#character-count");
const translateButton = document.querySelector("#translate-button");
const translateButtonLabel = document.querySelector("#translate-button-label");
const placeholderContent = document.querySelector("#result-placeholder-content");
const translationOutput = document.querySelector("#translation-output");
const sourceOutput = document.querySelector("#source-output");
const translatedOutput = document.querySelector("#translated-output");
const workspaceStatus = document.querySelector("#workspace-status");
const workspaceStatusText = document.querySelector("#workspace-status-text");

const directions = {
  "en-to-hi": {
    source: "English",
    target: "हिन्दी",
    targetCode: "hi",
    sourcePill: "ENGLISH",
    targetPill: "हिन्दी · HINDI",
    placeholder: "Type something in English…",
  },
  "hi-to-en": {
    source: "हिन्दी",
    target: "English",
    targetCode: "en",
    sourcePill: "हिन्दी · HINDI",
    targetPill: "ENGLISH",
    placeholder: "हिन्दी में कुछ लिखें…",
  },
};

let activeRequestId = 0;
let activeController = null;

function updateDirection() {
  const direction = directions[directionSelect.value];
  sourceLanguage.textContent = direction.source;
  targetLanguage.textContent = direction.target;
  targetLanguage.lang = direction.targetCode;
  sourcePill.textContent = direction.sourcePill;
  targetPill.textContent = direction.targetPill;
  sourceText.placeholder = direction.placeholder;
  updateInput();
}

function updateInput() {
  characterCount.textContent = `${sourceText.value.length} / ${sourceText.maxLength}`;
  translateButton.disabled = sourceText.value.trim().length === 0 || translateButton.classList.contains("is-loading");
}

function setStatus(message, state = "info") {
  workspaceStatusText.textContent = message;
  workspaceStatus.dataset.state = state;
}

function getApiUrl() {
  if (window.location.protocol === "http:" || window.location.protocol === "https:") {
    return `${window.location.origin}/api/translate`;
  }
  return "http://127.0.0.1:8000/api/translate";
}

async function translateText() {
  const source = sourceText.value.trim();
  if (!source) {
    setStatus("Enter text before translating.", "error");
    return;
  }

  if (activeController) activeController.abort();

  const requestId = ++activeRequestId;
  const controller = new AbortController();
  activeController = controller;
  translateButton.classList.add("is-loading");
  translateButton.disabled = true;
  translateButtonLabel.textContent = "Translating…";
  placeholderContent.hidden = true;
  translationOutput.hidden = false;
  sourceOutput.textContent = source;
  translatedOutput.textContent = "Translating…";
  setStatus("Translating your text locally…", "loading");

  try {
    const response = await fetch(getApiUrl(), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ direction: directionSelect.value, source_text: source }),
      signal: controller.signal,
    });
    const data = await response.json().catch(() => null);

    if (requestId !== activeRequestId) return;
    if (!response.ok) throw new Error(data?.message || "Translation could not be completed.");
    if (typeof data?.translated_text !== "string" || !data.translated_text.trim()) {
      throw new Error("The translation service returned no text.");
    }

    translatedOutput.textContent = data.translated_text;
    translatedOutput.lang = data.target_language === "hi" ? "hi" : "en";
    setStatus("Translation complete.", "success");
  } catch (error) {
    if (error.name === "AbortError" || requestId !== activeRequestId) return;
    sourceOutput.textContent = source;
    translatedOutput.textContent = "Translation unavailable";
    setStatus(error instanceof Error ? error.message : "Translation could not be completed.", "error");
  } finally {
    if (requestId === activeRequestId) {
      translateButton.classList.remove("is-loading");
      translateButtonLabel.textContent = "Translate text";
      activeController = null;
      updateInput();
    }
  }
}

directionSelect.addEventListener("change", () => {
  activeRequestId += 1;
  if (activeController) activeController.abort();
  activeController = null;
  translateButton.classList.remove("is-loading");
  translateButtonLabel.textContent = "Translate text";
  updateDirection();
  placeholderContent.hidden = false;
  translationOutput.hidden = true;
  translatedOutput.textContent = "";
  setStatus("Direction changed. Ready to translate.", "info");
});
sourceText.addEventListener("input", () => {
  updateInput();
  if (workspaceStatus.dataset.state === "error" || workspaceStatus.dataset.state === "success") {
    setStatus("Ready to translate.", "info");
  }
});
translateButton.addEventListener("click", translateText);

updateDirection();
