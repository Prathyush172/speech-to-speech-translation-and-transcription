# Implementation Plan --- AI-Mediated English ↔ Hindi Speech Translation

> **Purpose:** This file is the implementation contract for GitHub
> Copilot and the four-person student team. Follow it Scrum by Scrum, in
> order. Create the Jira backlog first; then implement one Scrum at a
> time, test it, review it, and merge it before starting the next
> dependent Scrum.
>
> **Project scope for this version:** Browser-based, local-first,
> **English → Hindi** and **Hindi → English** speech translation. A user
> speaks into the browser microphone; the system transcribes the source
> speech, translates the text, displays both transcripts, generates
> speech in the target language, and plays the audio. Other languages,
> multi-party calls, user accounts, cloud deployment, and advanced voice
> cloning are out of scope unless the instructor explicitly changes the
> scope.

------------------------------------------------------------------------

## 0. Mandatory workflow: Jira first, code second

### Jira backlog setup (do this before implementation)

Create a Jira Scrum project for **AI-Mediated Translation and
Transliteration**. Create **4 sprints**, with **exactly 10 Scrum backlog
items per sprint** (40 items total). Use the 40 items in Section 3 as
the backlog. Create each as a Story or Task according to your course
convention; keep the IDs/titles and acceptance criteria. Assign an
owner, add labels such as `sprint-1`, `backend`, `frontend`, `ml`,
`testing`, or `devops`, and add dependencies where indicated.

Recommended Jira fields: - Summary: use the exact item title from this
document. - Description: copy the item description and acceptance
criteria. - Sprint: Sprint 1, Sprint 2, Sprint 3, or Sprint 4. -
Assignee: use the team allocation below; rotate if workload differs. -
Labels: `english-hindi-translation` plus relevant component labels. -
Definition of Done: code merged to `main`, relevant tests pass,
README/docs updated where applicable, and the Jira item moved to Done. -
Do not create more than 40 backlog items for this plan. Subtasks are
optional only if the instructor allows them; they do not replace the 40
top-level items.

### Four-person team allocation

Use actual names in Jira, but keep these roles stable to reduce merge
conflicts:

-   **Member A --- Frontend & UX:** browser UI, language direction,
    microphone controls, transcript display, audio playback,
    accessibility.
-   **Member B --- Backend & API:** FastAPI app, request validation, API
    routes, WebSocket/session orchestration, error responses.
-   **Member C --- ML & Language pipeline:** speech recognition,
    English↔Hindi translation adapter, TTS adapter, model configuration
    and performance checks.
-   **Member D --- QA, integration & DevOps:** tests, fixtures/mocks,
    environment configuration, logging, GitHub integration,
    documentation and end-to-end validation.

All four members must review and test integrations; the roles are
primary ownership, not silos. Each task still needs one accountable
assignee.

### Sprint cadence

Each sprint contains exactly 10 backlog items. At sprint start, confirm
acceptance criteria and dependencies. During the sprint: 1. Pull the
latest `main`. 2. Create a short-lived feature branch for one Scrum
item. 3. Implement only that item and its necessary tests. 4. Run the
relevant tests and formatting/lint checks. 5. Commit with the Jira key
in the message. 6. Push the branch and open a pull request (PR). 7. A
different team member reviews the PR. 8. Merge only after checks pass;
pull the updated `main` before the next item.

At sprint end, demo the working increment, close only completed Jira
items, and tag the release checkpoint listed below.

------------------------------------------------------------------------

## 1. Product definition

### User stories

1.  As an English speaker, I want to speak English and hear a Hindi
    translation so I can communicate with a Hindi speaker.
2.  As a Hindi speaker, I want to speak Hindi and hear an English
    translation so I can communicate with an English speaker.
3.  As a user, I want to see the original transcript and translated text
    so I can confirm what the system heard and translated.
4.  As a user, I want clear status and error messages when microphone
    access, speech recognition, translation, or audio generation fails.

### Functional requirements

-   Support two directions: `en-to-hi` and `hi-to-en`.
-   Capture microphone audio in a browser only after the user explicitly
    grants permission.
-   Provide start, stop, and cancel/reset controls.
-   Transcribe the spoken source language.
-   Translate the source transcript into the target language.
-   Display source transcript and translated text.
-   Generate target-language speech and provide playback controls.
-   Show loading/progress states and recoverable errors.
-   Offer a typed-text fallback so the translation pipeline can be
    tested without a microphone.
-   Provide local API documentation and setup instructions.
-   Use mock adapters in automated tests so the test suite does not
    require model downloads or GPU access.

### Non-functional requirements

-   Run locally on Windows for development, with an NVIDIA RTX 3050 6 GB
    GPU and 16 GB RAM as the target hardware.
-   Do not send audio/text to external services by default. Models run
    locally unless the team explicitly documents and obtains approval
    for a remote service.
-   Keep model code behind interfaces/adapters; do not tie API routes
    directly to one model library.
-   Never commit model weights, generated audio, secrets, `.env`,
    virtual environments, or user recordings.
-   Handle long-running model calls without blocking the API event loop.
-   Log useful operational errors without logging raw audio or private
    transcript contents by default.
-   Use typed request/response schemas and consistent error responses.
-   Keep English/Hindi as the only supported language pair in this
    version.

### Architecture

``` text
Browser UI
  ├── language direction selector (English → Hindi / Hindi → English)
  ├── microphone capture + typed-text fallback
  ├── source transcript + translated text
  └── translated audio playback
          |
          | HTTP JSON / multipart upload
          v
FastAPI backend
  ├── validation + health endpoint
  ├── speech-to-text adapter
  ├── translation adapter (English ↔ Hindi)
  ├── text-to-speech adapter
  ├── orchestration/service layer
  └── audio response handling
          |
          v
Local model runtime(s)
  ├── STT: faster-whisper (start with a small model for hardware fit)
  ├── Translation: IndicTrans2-compatible implementation/model
  └── TTS: a verified Windows-compatible English/Hindi TTS implementation
```

**Important model rule:** do not invent a model identifier, assume a
model has a permissive license, or assume it supports Windows/GPU.
During Sprint 2, verify the chosen models' official setup instructions,
license, language coverage, Windows compatibility, and memory use. Keep
model implementations replaceable. If a model is not installable on the
target Windows setup, use a documented compatible alternative or a mock
for development; do not block the entire project on an unverified model.

### Suggested technology choices

-   Frontend: HTML/CSS/JavaScript or the existing course-approved
    frontend framework. Do not introduce a second frontend framework
    after the initial scaffold without team agreement.
-   Backend: Python 3.11, FastAPI, Uvicorn, Pydantic.
-   STT: `faster-whisper`; start with a small model and benchmark
    locally.
-   Translation: an IndicTrans2 implementation verified for
    English↔Hindi and Windows. Encapsulate it behind
    `TranslationProvider`.
-   TTS: choose and verify a Windows-compatible local engine supporting
    both English and Hindi; encapsulate it behind `TTSProvider`.
-   Tests: `pytest`, FastAPI `TestClient` or HTTPX; frontend tests can
    be lightweight manual checklists if no test framework is already
    established.
-   Version control: Git + GitHub PRs.
-   Jira: backlog, sprint planning, ownership, acceptance criteria, and
    Done status.

Do not add Docker as a prerequisite for the Windows-local version.
Docker can be introduced later only if the team decides it helps
reproducibility.

------------------------------------------------------------------------

## 2. Repository and code conventions

### Target repository structure

Build this structure incrementally; do not generate the entire
application in one huge Copilot change.

``` text
ai-mediated-translation/
├── README.md
├── IMPLEMENTATION.md
├── .gitignore
├── .env.example
├── requirements.txt
├── pyproject.toml
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   └── logging_config.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   └── translation.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── translation_service.py
│   │   ├── providers/
│   │   │   ├── __init__.py
│   │   │   ├── stt.py
│   │   │   ├── translation.py
│   │   │   └── tts.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── audio.py
│   └── tests/
│       ├── conftest.py
│       ├── test_health.py
│       ├── test_validation.py
│       ├── test_translation_service.py
│       └── test_api.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── README.md
├── docs/
│   ├── architecture.md
│   ├── api.md
│   ├── testing.md
│   └── demo-checklist.md
└── scripts/
    ├── setup_windows.ps1
    └── run_dev.ps1
```

The team may adjust the structure if the repository already contains a
working scaffold. Update this document and the architecture
documentation if any structure change is agreed.

### Code rules

-   Keep route handlers thin. Model logic belongs in provider classes
    and services.
-   Define interfaces/protocols for STT, translation, and TTS providers.
-   Do not load large models on every request. Initialize providers once
    on application startup or lazily once with a safe singleton.
-   Do not execute blocking model inference directly on the async event
    loop. Use a worker thread/process or appropriate async integration.
-   Validate direction against exactly `en-to-hi` or `hi-to-en`.
-   Use clear, stable JSON response schemas.
-   Write tests with fake providers; keep a separate optional smoke test
    for actual models.
-   Never check generated audio or model cache directories into Git.
-   Use `pathlib` for file paths and temporary files; clean temporary
    audio after use.
-   Avoid exposing arbitrary filesystem paths or accepting unsafe
    filenames from requests.

------------------------------------------------------------------------

## 3. The 40 Jira Scrum items (4 sprints × 10 items)

The titles below are the exact Jira summaries. Create these items in
Jira **before coding**.

# Sprint 1 --- Foundation, requirements and project skeleton

**Sprint goal:** A clean repository, agreed architecture, working
backend/frontend skeleton, basic checks, and a team workflow everyone
can run locally.

### S1-01 --- Create repository and project baseline — **Completed**

**Owner:** Member D\
**Description:** Create the GitHub repository, default branch, initial
README, `.gitignore`, and the agreed folder structure.\
**Acceptance criteria:** - Repository contains the target folders from
Section 2 or a documented equivalent. - `.gitignore` excludes `.env`,
virtual environments, caches, generated audio, model weights, and build
artifacts. - README states project scope and English↔Hindi-only
limitation. - All four members can clone the repository.

### S1-02 --- Create Jira backlog and four sprints — **Completed**

**Owner:** Member D\
**Description:** Create all 40 items from this section, grouped into
four sprints of 10. Assign initial owners and labels.\
**Acceptance criteria:** - Exactly four sprints exist and each contains
10 top-level items. - All items have a description and acceptance
criteria. - Dependencies and labels are recorded. - Team confirms the
sprint order before implementation.

### S1-03 --- Finalize requirements and acceptance tests — **Completed**

**Owner:** Member A\
**Description:** Write the concise functional/non-functional
requirements and the user journeys for both directions.\
**Acceptance criteria:** - English→Hindi and Hindi→English flows are
separately documented. - Typed-text fallback is included. - Out-of-scope
features are explicitly listed. - Team and instructor-facing demo
criteria are documented.

### S1-04 --- Document architecture and provider boundaries — **Completed**

**Owner:** Member B\
**Description:** Create `docs/architecture.md` describing browser, API,
service layer, and STT/translation/TTS providers.\
**Acceptance criteria:** - Architecture diagram matches Section 1. -
Each model component has a replaceable provider boundary. -
Request/response flow and error handling are documented. - No
model-specific code is required by route handlers.

### S1-05 --- Set up Python environment and dependencies — **Completed**

**Owner:** Member C\
**Description:** Add a minimal Python 3.11 backend environment and pin
compatible core dependencies.\
**Acceptance criteria:** - Setup instructions create and activate a
virtual environment on Windows. - FastAPI, Uvicorn, Pydantic, pytest,
and HTTP client dependencies are listed. - Heavy ML dependencies are
separated or documented so a clean install can run tests without
downloading models. - No machine-specific absolute paths are committed.

### S1-06 --- Add environment configuration — **Completed**

**Owner:** Member B\
**Description:** Add typed settings for host, port, log level, model
IDs/paths, device selection, and upload limits.\
**Acceptance criteria:** - `.env.example` contains safe example values
only. - `.env` is ignored by Git. - Application has sensible local
defaults. - Invalid configuration produces a readable startup error.

### S1-07 --- Implement FastAPI application entry point — **Completed**

**Owner:** Member B\
**Description:** Create `backend/app/main.py`, app initialization,
startup/shutdown hooks, and API router registration.\
**Acceptance criteria:** - App starts with the documented Uvicorn
command. - `/docs` is available. - Startup does not download models
unexpectedly. - Importing the app does not require a GPU.

### S1-08 --- Implement health endpoint and basic API tests — **Completed**

**Owner:** Member D\
**Description:** Add `GET /api/health` and tests for app startup and
health response.\
**Acceptance criteria:** - Endpoint returns JSON indicating service
status. - Automated test passes without model downloads. - Failure
output is understandable. - Test command is documented.

### S1-09 --- Build initial browser UI shell — **Completed**

**Owner:** Member A\
**Description:** Create responsive page structure with project title,
direction selector, mic/start/stop controls, typed-text fallback,
transcript panels, and audio player placeholder.\
**Acceptance criteria:** - Layout works on desktop browser. - Both
language directions are selectable. - Controls have labels and
disabled/loading states. - No model/API calls are required for this
scaffold.

### S1-10 --- Establish Git branching, PR and review rules — **Completed**

**Owner:** Member D\
**Description:** Document shared Git workflow and ensure every member
can create a branch and open a PR.\
**Acceptance criteria:** - `main` is protected if repository permissions
allow. - PR template/checklist exists or the README contains the
equivalent. - Each member makes one small test PR or contributes a
reviewed change. - Team agrees never to force-push shared `main`.

The workflow documentation and PR template were merged to `main` in PR
#8. Branch protection is configured separately by a repository
administrator if repository permissions allow.

**Sprint 1 release checkpoint --- `v0.1-foundation`:** Merge all
accepted changes, run tests, tag the commit, and confirm all four
members can pull and run the skeleton.

------------------------------------------------------------------------

# Sprint 2 --- Working text pipeline and model adapters

**Sprint goal:** The user can submit typed English or Hindi text and
receive translated text through the API, while model providers are
independently testable.

### S2-01 --- Define request and response schemas

**Owner:** Member B\
**Description:** Add Pydantic schemas for direction, source text,
detected/source language, translated text, processing status, and error
payloads.\
**Acceptance criteria:** - Only `en-to-hi` and `hi-to-en` are
accepted. - Empty/whitespace text is rejected with a useful 4xx
response. - Response fields are documented. - Schema tests cover valid
and invalid input.

### S2-02 --- Define STT, translation and TTS provider interfaces

**Owner:** Member C\
**Description:** Define clear provider interfaces in
`backend/app/providers/` with methods and typed return values.\
**Acceptance criteria:** - STT accepts audio input and returns
transcript plus language/metadata where available. - Translation accepts
text and direction and returns translated text. - TTS accepts text and
target language and returns audio bytes or a managed audio artifact. -
Tests can inject fake providers without loading ML packages.

### S2-03 --- Implement fake providers for development

**Owner:** Member C\
**Description:** Implement deterministic fake STT, translation, and TTS
providers for API tests and early UI integration.\
**Acceptance criteria:** - Fake providers are clearly marked
development/test-only. - Tests do not claim fake output is a real
translation. - App can be run in mock mode from configuration. - No
network or model download is required in mock mode.

### S2-04 --- Verify and document Windows-compatible STT model

**Owner:** Member C\
**Description:** Evaluate `faster-whisper` model options for
English/Hindi on Windows and the target GPU/CPU setup.\
**Acceptance criteria:** - Official setup and license are checked. - A
small model is selected for the first local smoke test. - CPU/GPU mode
and VRAM/RAM observations are recorded. - Model loading is optional and
isolated behind the STT provider.

### S2-05 --- Implement faster-whisper STT adapter

**Owner:** Member C\
**Description:** Implement audio-to-transcript conversion with clear
language handling and errors.\
**Acceptance criteria:** - Adapter conforms to the STT interface. -
Supports English and Hindi input. - Handles invalid/empty audio. - Unit
tests use a mock; an optional local smoke test verifies real inference.

### S2-06 --- Verify and document English↔Hindi translation model

**Owner:** Member C\
**Description:** Verify an IndicTrans2 implementation that supports both
directions and can be installed in the team's Windows environment.\
**Acceptance criteria:** - Model source, license, install steps, and
language codes are documented. - One short English→Hindi and one
Hindi→English example are manually checked. - Model loading/memory needs
are recorded. - If the preferred implementation is incompatible, the
team records a compatible replacement rather than blocking other work.

### S2-07 --- Implement translation provider adapter

**Owner:** Member C\
**Description:** Implement the real translation adapter behind the
provider interface.\
**Acceptance criteria:** - Both directions are supported. -
Direction-to-source/target language mapping is centralized. - Empty
output and model exceptions are handled. - Unit tests cover both
directions using fixtures/mocks; real-model checks are separate.

### S2-08 --- Implement text translation service

**Owner:** Member B\
**Description:** Orchestrate request validation, source/target mapping,
translation provider call, response construction, and timing metadata.\
**Acceptance criteria:** - Service has no dependency on FastAPI request
objects. - Provider errors become controlled service errors. - Unit
tests cover success and failure paths. - Logs do not print full user
text by default.

### S2-09 --- Add `POST /api/translate` endpoint

**Owner:** Member B\
**Description:** Expose typed-text translation as a JSON API.\
**Acceptance criteria:** - Endpoint returns source text, direction,
target text, and status. - Invalid direction/text returns useful 4xx
errors. - Provider failure returns a safe 5xx response without stack
traces to the client. - OpenAPI docs show the request and response
shape.

### S2-10 --- Connect typed-text UI to translation API

**Owner:** Member A\
**Description:** Wire the text box and direction selector to
`/api/translate`; display source and translated text.\
**Acceptance criteria:** - User can translate typed text in both
directions. - Loading and error states are visible. - Rapid repeat
clicks do not corrupt the displayed result. - Manual test steps are
added to `docs/demo-checklist.md`.

**Sprint 2 release checkpoint --- `v0.2-text-translation`:** Demonstrate
typed English→Hindi and Hindi→English. Run all unit/API tests. Push and
merge only after a second member reviews the PRs.

------------------------------------------------------------------------

# Sprint 3 --- Speech input and translated speech output

**Sprint goal:** Complete the main speech workflow from browser
microphone audio through STT, translation, TTS, and audio playback.

### S3-01 --- Verify Windows-compatible English/Hindi TTS options

**Owner:** Member C\
**Description:** Evaluate a local TTS engine/model for both English and
Hindi. Do not assume a model requiring Apple's MLX runtime works on
Windows.\
**Acceptance criteria:** - Model supports the needed languages and has a
reviewed license. - Installation works on Windows or an explicitly
documented supported runtime. - At least one English and one Hindi
sample are generated. - Memory, startup time, synthesis latency, and
voice quality observations are documented.

### S3-02 --- Implement TTS provider adapter

**Owner:** Member C\
**Description:** Implement text-to-speech behind the TTS provider
interface.\
**Acceptance criteria:** - Accepts target text and language. - Returns
valid audio data with a known format/content type. - Handles unsupported
language, empty text, and synthesis failures. - Unit tests use a fake
provider; actual model test is optional/local.

### S3-03 --- Add safe audio input validation and utilities

**Owner:** Member B\
**Description:** Validate uploaded audio type, size, duration where
feasible, and safely manage temporary files/conversion.\
**Acceptance criteria:** - Configured maximum upload size is enforced. -
Unsupported/empty audio returns a clear client error. - Temporary files
are cleaned up on success and failure. - Client-supplied filenames are
never used as filesystem paths.

### S3-04 --- Add `POST /api/speech-to-text` endpoint

**Owner:** Member B\
**Description:** Accept audio upload and return transcript,
language/direction metadata, and status.\
**Acceptance criteria:** - Supports English and Hindi input. - Handles
invalid media and STT failures cleanly. - Response shape is
documented. - Tests cover mocked success and failure.

### S3-05 --- Add `POST /api/speech-translate` orchestration endpoint

**Owner:** Member B\
**Description:** Accept source audio and direction, call STT then
translation then TTS, and return text metadata plus generated audio in a
documented response strategy.\
**Acceptance criteria:** - Both directions are supported. - Source
transcript and translated text are available to the client. - Audio is
returned as a file response or via a documented job/result flow; do not
invent a mixed JSON/binary format. - Errors identify the failed stage
without exposing internal traces.

### S3-06 --- Implement browser microphone permission and capture

**Owner:** Member A\
**Description:** Capture microphone audio only after explicit user
action and handle browser permission denial.\
**Acceptance criteria:** - Start/stop controls work in a supported
browser. - Permission denial displays instructions and does not crash
the UI. - Recording indicator is visible while recording. - Audio is
stopped and media tracks are released when recording ends or page state
resets.

### S3-07 --- Upload captured audio and show source transcript

**Owner:** Member A\
**Description:** Send captured audio to the backend with the chosen
direction and display the source transcript.\
**Acceptance criteria:** - Correct direction is sent with every
request. - User sees progress while processing. - Source transcript is
displayed separately from translated text. - Network/API errors are
recoverable.

### S3-08 --- Play generated translated audio

**Owner:** Member A\
**Description:** Handle the generated audio response and provide
play/pause/replay controls.\
**Acceptance criteria:** - Successful response can be played in the
browser. - Previous audio URLs/resources are cleaned up when replaced. -
Audio format and content type match the API contract. - Failed playback
shows a useful message.

### S3-09 --- Add cancellation, reset and duplicate-request protection

**Owner:** Member A\
**Description:** Prevent accidental duplicate submissions and let the
user reset the current result.\
**Acceptance criteria:** - Submit is disabled or guarded while a request
is active. - Reset clears visible transcripts/errors and stops audio
playback. - Late responses do not overwrite a newer request. -
Cancellation is implemented only where supported and documented.

### S3-10 --- Run speech pipeline integration tests

**Owner:** Member D\
**Description:** Add integration tests using fake providers and manual
smoke tests with real local models.\
**Acceptance criteria:** - Tests verify audio input → transcript →
translated text → audio response using fakes. - Both directions are
tested. - Manual checklist covers microphone denial, invalid audio, slow
model, and successful playback. - Actual-model smoke test instructions
are separate from the default test suite.

**Sprint 3 release checkpoint --- `v0.3-speech-pipeline`:** Demonstrate
a full English→Hindi and Hindi→English speech round trip. Run automated
tests and the manual model smoke test. Document known latency/quality
limitations.

------------------------------------------------------------------------

# Sprint 4 --- Quality, reliability, documentation and final demo

**Sprint goal:** Deliver a robust mini-project that can be cloned,
installed, tested, demonstrated, and evaluated by the instructor.

### S4-01 --- Improve end-to-end UI states and accessibility

**Owner:** Member A\
**Description:** Polish responsive layout, labels, keyboard navigation,
loading indicators, transcript separation, and errors.\
**Acceptance criteria:** - All controls have visible labels. - Focus
indicators and keyboard operation are usable. - Loading/success/error
states are distinguishable. - Desktop demo layout is clean and readable.

### S4-02 --- Add request timeout and model failure handling

**Owner:** Member B\
**Description:** Add controlled timeout behavior and stable error
mapping for STT, translation, and TTS failures.\
**Acceptance criteria:** - Client receives a stable error schema. - No
Python stack trace or sensitive local path is returned. - Timeout and
provider errors are logged with request correlation IDs. - Tests cover
each stage's failure.

### S4-03 --- Add structured logging and timing metrics

**Owner:** Member B\
**Description:** Record request IDs, stage timings, outcome, and
provider errors without recording raw audio or full transcript by
default.\
**Acceptance criteria:** - Logs distinguish STT, translation, and TTS
timing. - Sensitive payloads are not logged by default. - Logs are
useful for diagnosing failures. - Documentation explains where local
logs are written.

### S4-04 --- Add translation and transcription evaluation set

**Owner:** Member D\
**Description:** Create a small, consent-safe set of short English/Hindi
test phrases and expected translations/transcripts for regression
checks.\
**Acceptance criteria:** - Includes both directions, short/long
sentences, punctuation, numbers, and common names. - Dataset contains no
private recordings or personal data. - Expected outputs are reviewed by
a competent Hindi/English speaker. - Evaluation is documented as a small
demo set, not a scientific benchmark.

### S4-05 --- Add performance and memory benchmark script

**Owner:** Member C\
**Description:** Measure warm and cold model startup, per-stage latency,
and peak memory for representative short utterances.\
**Acceptance criteria:** - Script records environment, selected model
IDs, device, and timing. - At least five short examples are measured for
each direction when hardware allows. - Report identifies CPU/GPU
configuration and limitations. - No hard performance guarantee is
claimed without measurements.

### S4-06 --- Harden input and temporary-file handling

**Owner:** Member B\
**Description:** Review upload limits, file type validation, temporary
file cleanup, CORS, and error messages.\
**Acceptance criteria:** - Only intended local frontend origins are
allowed in development CORS configuration. - Upload size and type checks
are tested. - Temporary files are cleaned even when inference fails. -
No endpoint exposes arbitrary filesystem access.

### S4-07 --- Write Windows setup and troubleshooting guide

**Owner:** Member D\
**Description:** Document a clean Windows setup, model downloads,
environment variables, run commands, and common errors.\
**Acceptance criteria:** - A teammate can follow the README on a clean
clone. - Includes venv activation, dependency installation, backend
start, frontend start, and tests. - Explains model download/cache and
GPU fallback. - Documents the MLX incompatibility lesson and states that
Apple-only runtime models must not be selected.

### S4-08 --- Complete API and user documentation

**Owner:** Member B\
**Description:** Document endpoints, request/response examples,
architecture, limitations, and data handling.\
**Acceptance criteria:** - API docs match actual implementation. - Setup
and run instructions match current commands. - English↔Hindi scope and
out-of-scope features are clear. - Known limitations and troubleshooting
are included.

### S4-09 --- Run full regression and acceptance checklist

**Owner:** Member D\
**Description:** Run automated tests and execute the final demo
checklist on the target Windows machine.\
**Acceptance criteria:** - All default automated tests pass. - Both
directions work through typed-text and speech workflows. - Microphone
denial, invalid input, and model failure are tested. - Any remaining
known bug is documented and linked to Jira.

### S4-10 --- Prepare final demo, release tag and handoff

**Owner:** Member A (demo lead), all members contribute\
**Description:** Prepare a repeatable demo script, final architecture
diagram, team contribution summary, and release tag.\
**Acceptance criteria:** - Demo shows both English→Hindi and
Hindi→English. - Repository has no secrets, model weights, private
recordings, or generated test artifacts committed. - `main` is green and
all accepted work is merged. - Release tag `v1.0.0` is created and final
setup/demo steps are documented.

**Sprint 4 release checkpoint --- `v1.0.0`:** Freeze scope, run final
regression, demo the product, and hand off the repository and
documentation.

------------------------------------------------------------------------

## 4. GitHub collaboration rules (mandatory for all 4 members)

### Branch naming

Use one branch per Jira item:

``` text
feature/<JIRA-KEY>-short-description
fix/<JIRA-KEY>-short-description
docs/<JIRA-KEY>-short-description
test/<JIRA-KEY>-short-description
```

Example: `feature/AMTT-17-translation-endpoint`

### Start every task by pulling

Run from the repository root:

``` powershell
git switch main
git pull origin main
git switch -c feature/<JIRA-KEY>-short-description
```

Replace the placeholder with the actual Jira key and a short
description. Never run the literal placeholder command.

### Before committing

``` powershell
git status
git diff --check
```

Run the tests relevant to your change. For backend changes, activate the
venv and run:

``` powershell
python -m pytest
```

Then commit and push:

``` powershell
git add <specific-files>
git commit -m "<JIRA-KEY>: describe the change"
git push -u origin feature/<JIRA-KEY>-short-description
```

Replace placeholders. Prefer adding specific files instead of
`git add .` when generated files may exist.

### Pull request and merge

1.  Open a PR into `main`.
2.  Include the Jira key, summary, tests run, screenshots or API
    examples where useful, and any setup changes.
3.  A different team member reviews the code.
4.  Resolve review comments and rerun tests.
5.  Merge the PR only when checks pass, using GitHub's **Squash and
    merge** option to avoid merge commits.
6.  Delete the feature branch after merge if GitHub permits.
7.  The task owner runs `git switch main` and `git pull origin main`
    before starting another item.

### If `main` changes while working

Before opening/merging a PR, sync your branch with the latest `main`
before publishing it, using rebase so the feature branch does not add a
merge commit:

``` powershell
git fetch origin
git rebase origin/main
```

Resolve conflicts carefully and rerun tests before pushing. If the branch
was already published and the rebase would require a force push, do not
force-push; coordinate with the reviewer and create a fresh branch if
needed. Never force-push shared `main`. Do not overwrite another member's
work to resolve a conflict; ask the author when intent is unclear.

### Pull request checklist and branch protection

The repository includes `.github/PULL_REQUEST_TEMPLATE.md` with the
required summary, test evidence, and review checklist. Repository
administrators should enable protection for `main` in GitHub settings,
requiring at least one approving review and preventing force pushes and
branch deletion. Branch protection is a repository permission and must be
confirmed by an administrator; contributors must not assume it is enabled.

### Sprint checkpoint commits and tags

At the end of each sprint, after all sprint items are merged and tests
pass:

``` powershell
git switch main
git pull origin main
python -m pytest
git tag -a v0.1-foundation -m "Sprint 1 foundation"
git push origin v0.1-foundation
```

Use the corresponding tag for later checkpoints:
`v0.2-text-translation`, `v0.3-speech-pipeline`, and `v1.0.0`. Only one
team member should create/push a given tag, after confirming with the
team that the release commit is correct.

### What to do if someone accidentally commits to `main`

Stop and coordinate. Do not reset or force-push shared `main`. Open a
follow-up fix branch or ask the repository administrator to help recover
safely.

------------------------------------------------------------------------

## 5. Definition of Done for every Scrum item

A Jira item is Done only when all applicable points are satisfied:

-   [ ] Acceptance criteria are met.
-   [ ] Implementation is scoped to the item; unrelated refactoring is
    avoided.
-   [ ] Automated tests are added/updated and pass.
-   [ ] Manual verification is performed when UI/audio/model behavior
    cannot be fully tested automatically.
-   [ ] No secrets, model weights, private recordings, or generated
    artifacts are committed.
-   [ ] Error paths and basic input validation are handled.
-   [ ] Relevant README/API/architecture docs are updated.
-   [ ] Branch is pushed and a PR is reviewed by another member.
-   [ ] PR is merged to `main`.
-   [ ] Jira item is moved to Done and includes the PR/commit link.

------------------------------------------------------------------------

## 6. Instructions specifically for GitHub Copilot

Copilot should use this file as the implementation sequence and follow
these constraints:

1.  **Do not implement all 40 items in one response or one change.**
    Work on exactly one Jira Scrum item at a time.
2.  At the start, inspect the repository and report which Scrum item is
    next. Do not overwrite existing working code without explaining why.
3.  If the repository is empty, implement S1-01 first, then stop for
    review before continuing.
4.  Before coding an item, summarize its acceptance criteria and list
    the files likely to change.
5.  Implement the smallest coherent change that satisfies the current
    item's acceptance criteria.
6.  Add or update tests in the same change.
7.  Run available checks and report exact commands and results. Never
    claim tests passed if they were not run.
8.  If model installation, hardware support, licensing, or an API is
    uncertain, inspect official documentation or leave a clearly marked
    adapter/configuration boundary. Do not fabricate model IDs, command
    flags, package APIs, or test results.
9.  Use fake providers for normal automated tests. Do not download
    gigabytes of model weights as a side effect of running unit tests.
10. Do not store secrets, recordings, model weights, or user data in
    Git.
11. After completing one Scrum item, provide: (a) summary, (b) files
    changed, (c) tests run and results, (d) manual verification
    steps, (e) Git commands for the owner, (f) Jira status
    recommendation, and (g) the next Scrum item. Then wait for the team
    to confirm before implementing the next item.
12. Do not skip Jira-first planning, code review, GitHub push/pull
    checkpoints, or sprint release checkpoints.
13. Keep the project English↔Hindi only. Do not add Kannada, Tamil,
    Telugu, multi-party calls, authentication, or cloud deployment
    without explicit approval.
14. Do not claim that a simple text transliteration is the same as
    translation. For this version, the main flow is speech recognition →
    translation → speech synthesis. Transliteration can be added as a
    separately scoped feature if required by the instructor; it is not a
    substitute for translation.
15. Do not expose private machine paths in committed code. Use
    configuration and relative paths.

### Copilot prompt to start implementation

Paste this prompt into Copilot Chat after adding this file to the
repository:

> Read `IMPLEMENTATION.md` completely. We are a four-member student team
> implementing the English↔Hindi AI-Mediated Translation project. Follow
> the Jira-first process and do not implement all sprints at once. First
> inspect the current repository. If it is empty, implement **S1-01
> only**: repository/project baseline and folder structure. Create only
> the files needed for S1-01, make sure `.gitignore` excludes secrets,
> virtual environments, model weights, caches, and generated audio, and
> write a concise README with the project scope. Do not implement model
> inference or later Scrum items yet. Report changed files, checks run,
> and the next Git commands. Wait for approval before starting S1-02 or
> any other item.

------------------------------------------------------------------------

## 7. Sprint review gates

### End of Sprint 1

-   [ ] Jira contains 40 items in 4 sprints, 10 per sprint.
-   [ ] Repository structure exists and every member can clone it.
-   [ ] FastAPI health endpoint works.
-   [ ] Initial frontend shell renders.
-   [ ] Tests run without downloading ML models.
-   [ ] Tag `v0.1-foundation` pushed.

### End of Sprint 2

-   [ ] Typed English→Hindi translation works.
-   [ ] Typed Hindi→English translation works.
-   [ ] Fake-provider tests pass.
-   [ ] Real translation model setup is documented and verified or an
    explicit fallback decision is recorded.
-   [ ] Tag `v0.2-text-translation` pushed.

### End of Sprint 3

-   [ ] Browser microphone flow works with permission granted.
-   [ ] Speech-to-text works for both languages on the test machine.
-   [ ] Translated text is visible.
-   [ ] Target-language audio can be played.
-   [ ] Invalid audio and provider failures show understandable errors.
-   [ ] Tag `v0.3-speech-pipeline` pushed.

### End of Sprint 4

-   [ ] Both directions pass the demo checklist.
-   [ ] Tests, setup guide, architecture and API docs are current.
-   [ ] All four members' work is merged and reviewable in Git history.
-   [ ] No secrets, model weights, or private recordings are tracked.
-   [ ] Tag `v1.0.0` pushed.

------------------------------------------------------------------------

## 8. Scope guard and known risks

-   **Local inference risk:** Large models may not fit entirely in 6 GB
    VRAM. Use small/quantized options where officially supported,
    consider CPU fallback, and measure latency.
-   **Windows compatibility risk:** Some TTS projects depend on macOS
    MLX or Linux-only scripts. Verify Windows support before choosing a
    model.
-   **Model license risk:** Check the actual model and code licenses
    before including them in a public repository or demo.
-   **Translation quality risk:** English↔Hindi output should be checked
    with a reviewed test set; do not claim perfect translation.
-   **Browser audio risk:** Microphone capture requires user permission
    and works most reliably on `localhost` or HTTPS.
-   **Latency risk:** Initial model load can be slow. Load models once
    and report cold-start versus warm-request timing.
-   **Feature boundary:** This plan implements English↔Hindi speech
    translation. General transliteration, live full-duplex conversation,
    meeting recording, accounts, cloud hosting, and additional languages
    are future work unless explicitly added to Jira.

**Final rule:** Jira defines the Scrum items, this file defines the
order and acceptance criteria, GitHub PRs are the integration gate, and
`main` must always remain in a runnable state.
