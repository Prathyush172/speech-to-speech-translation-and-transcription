<div align="center">

# Speech-to-Speech Translation and Transcription

### Local-first speech translation and transcription for English and Hindi

![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)
![Language pair](https://img.shields.io/badge/Language-English%20%E2%86%94%20Hindi-4C8EDA)
![Local-first](https://img.shields.io/badge/Processing-Local--first-2E8B57)

[Overview](#scope) · [How it works](docs/architecture.md) · [Setup](#getting-started) · [API docs](docs/api.md)

</div>

---

A browser-based application that accepts microphone audio or typed text and
translates in two directions: English → Hindi and Hindi → English. The browser
displays the source transcript and translated text and can play generated
target-language audio.

## Scope

This project intentionally supports English and Hindi only. It does not
include other languages, multi-party calls, user accounts, cloud
deployment, or voice cloning. Audio and text are intended to stay local;
do not send them to external services unless the team explicitly documents
and approves that integration.

## Repository layout

- `backend/` — FastAPI application, provider boundaries, service logic,
  schemas, and backend tests.
- `frontend/` — browser UI, styles, and client-side interaction code.
- `docs/` — requirements, architecture, API, testing, and demonstration
  guidance. See [requirements and acceptance tests](docs/requirements.md)
  and [architecture and provider boundaries](docs/architecture.md).
- `scripts/` — local development and Windows setup helpers.
- `IMPLEMENTATION.md` — the Scrum implementation contract and backlog
  for the full project.

## Getting started

The repository is designed to work on Windows with Python 3.11.

```powershell
git clone https://github.com/Kushal-phbs/speech-to-speech-translation-and-transcription.git
cd speech-to-speech-translation-and-transcription
./scripts/setup_windows.ps1
.\.venv\Scripts\Activate.ps1
python -m pytest
```

The setup script requires Python 3.11, creates `.venv`, and installs the
runtime and test dependencies. Heavy STT, translation, and TTS packages are
not included in the default setup; they are listed separately in
`requirements-ml.txt` and must only be installed when an actual model adapter
is implemented. The application uses local defaults; copy `.env.example` to
`.env` to override the host, port, log level, model IDs/cache path, device, or
maximum upload size. Invalid values are reported with the setting name when the
application starts. `.env` and other environment-specific files are ignored by
Git.

Start the API from the repository root with:

```powershell
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
```

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.
Application startup initializes only configuration and logging; speech models
are not loaded or downloaded.
The `GET /api/health` endpoint returns `{"status": "ok"}`. Run its API tests
from the repository root with `python -m pytest`.

The UI scaffold can be previewed by opening `frontend/index.html` in a desktop
browser. Direction selection and text character count work locally; microphone,
translation, and audio controls remain disabled until those features are wired
to the API.

## Project workflow

Contributors should work on one short-lived branch per Scrum item, based on
the latest `main`, and open a pull request for each completed item. Never
commit or push directly to shared `main`, and never force-push it. Rebase a
feature branch before publishing if `main` has moved; use GitHub's **Squash and
merge** option to avoid merge commits. A different team member should review
the pull request and approve it before it is merged.

```powershell
git switch main
git pull --ff-only origin main
git switch -c feature/AMTT-<number>-short-description
# Make and test the change, then commit only the relevant files.
git push -u origin feature/AMTT-<number>-short-description
```

Replace the example branch name with the task's Jira key and a short
description. Use the pull request checklist in
[`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md).
Repository administrators should protect `main` by requiring an approving
review and preventing force pushes and branch deletion. This repository's
branch protection must be enabled in GitHub settings by an administrator.

## Current status

- [x] AMTT-1 — Repository and project baseline completed.
- [x] AMTT-2 — Jira backlog, sprint structure, and export completed.
- [x] AMTT-3 — Requirements and acceptance tests.
- [x] AMTT-4 — Architecture and provider boundaries.
- [x] AMTT-5 — Python environment and dependencies.
- [x] AMTT-6 — Environment configuration.
- [x] AMTT-7 — FastAPI application entry point.
- [x] AMTT-8 — Health endpoint and API tests.
- [x] AMTT-9 — Initial browser UI shell.
- [x] AMTT-10 — Git branching, PR, and review rules.

All ten Sprint 1 Scrum items are complete. The separate `v0.1-foundation`
release checkpoint remains pending until its tag is created and all four
members confirm they can pull and run the skeleton. See `IMPLEMENTATION.md`
for the checkpoint steps.

## Sprint 2 checklist — Working text pipeline and model adapters

- [ ] S2-01 — Define request and response schemas.
- [ ] S2-02 — Define STT, translation and TTS provider interfaces.
- [ ] S2-03 — Implement fake providers for development.
- [ ] S2-04 — Verify and document Windows-compatible STT model.
- [ ] S2-05 — Implement faster-whisper STT adapter.
- [ ] S2-06 — Verify and document English↔Hindi translation model.
- [ ] S2-07 — Implement translation provider adapter.
- [ ] S2-08 — Implement text translation service.
- [ ] S2-09 — Add `POST /api/translate` endpoint.
- [ ] S2-10 — Connect typed-text UI to translation API.

Sprint 2's `v0.2-text-translation` release checkpoint is described in
`IMPLEMENTATION.md`.
Thank YOU
