# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
