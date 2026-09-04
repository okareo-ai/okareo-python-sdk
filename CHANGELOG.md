# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Client-level Project (project separation): `Okareo(..., project=...)` and
  `set_project()` scope every call without repeating `project_id`; precedence is
  per-call / explicitly-set field, then client-level, then the server default.
  Both accept a Project **name** or its id — `Okareo(api_key=KEY, project="Support Team")`
  — since Project names are unique per organization. Names match case-insensitively
  and ignore surrounding whitespace. A name or id that matches nothing fails at
  construction with a message listing every available Project.
- Project lifecycle: `get_project()`, `update_project()`, `archive_project()`,
  `unarchive_project()`.
  Archiving is reversible and only hides a Project from the picker — it restricts
  nothing. The default ("Global") Project cannot be renamed or archived.
- `create_project()` and `update_project()` reject a Project name with leading or
  trailing whitespace locally, before the request — the same rule the server
  applies, without the round trip.

### Changed

- Once the project-separation backend is deployed, search endpoints that
  previously returned organization-wide results when `project_id` was omitted
  (`find_datapoints`, `find_datapoints_filter`, `find_test_runs`, and voice
  integration listing) resolve to the **default Project** instead. Every
  organization currently has exactly one Project, so existing scripts see the
  same data — but scripts that relied on omitted-project meaning "everything"
  should pass an explicit `project_id` once they use multiple Projects.
- `ingest_conversations` accepts an omitted `project_id` when a client-level
  Project is set, and raises a clear error when neither is available.

### Removed

- `OpenAIAssistantModel` and the `openai_assistant` Target type. OpenAI shut down the
  Assistants API on 2026-08-26 — `/v1/assistants`, `/v1/threads`, and `/v1/threads/runs`
  now return errors, with no grace period — so this Target type can no longer run.
  Use `GenerationModel` for a prompt-driven OpenAI Target, or `CustomEndpointTarget`
  to point at a hosted agent.
- References to retired predefined checks (`is_best_option`, `is_code_functional`,
  `does_code_compile`, `contains_all_imports`), which are no longer available in
  the Okareo platform.

### Fixed

- `run_simulation(..., tags=[...])` now applies the tags to the test run it creates.
  They were previously accepted and silently discarded, so the run came back with
  `tags: []` and was not findable via `find_test_runs(tags=[...])`.
  `ModelUnderTest.run_test` / `submit_test` also accept `tags` now.
- Example code-based check fixtures now declare `check_type` explicitly, matching the
  output-type requirement for code-based checks (a check returning `CheckResponse`
  otherwise fails output-type inference).

## [0.0.133] - 2026-06-09

### Added

- Voice SDK methods: generate_driver_prompt, find_test_runs, re_evaluate, download_call_recording
- PhoneTarget for simplified phone/voice target registration
- Augmentation parameter support in run_simulation
- Voice monitoring and augmentation interfaces

### Fixed

- Raw httpx methods now honor base_path constructor argument
- find_datapoints methods raise on ErrorResponse instead of returning it

[Unreleased]: https://github.com/okareo-ai/okareo-python-sdk/compare/v0.0.133...HEAD
[0.0.133]: https://github.com/okareo-ai/okareo-python-sdk/compare/v0.0.132...v0.0.133
