# Tasks: Filter Contribution Types for Contributor Card

**Input**: Design documents from `/specs/003-filter-contrib-types/`
**Prerequisites**: plan.md, spec.md, data-model.md, research.md

## Phase 1: Setup & Configuration

**Purpose**: Prepare the configuration structures and constants for the feature

- [x] T001 Define `VALID_CONTRIB_TYPES` constant in `src/core/constants.py` (or directly in `src/core/config.py`)
- [x] T002 Update `ContribFetchConfig` in `src/core/config.py` to include `contribution_types: list[str]` with a default value
- [x] T003 Update config instantiation in `src/core/config.py` to properly handle and parse comma-separated strings for the new `types` argument

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Update core data fetching logic to respect the new configuration parameter

- [x] T004 Modify GraphQL query generation in `src/github/fetcher.py` (`_async_process_year_contributions`) to conditionally include/exclude query blocks for commits, PRs, issues, and reviews
- [x] T005 Add unit tests in `tests/test_fetcher.py` to verify the generated GraphQL queries correctly respect the `contribution_types` filter

**Checkpoint**: Core data fetching logic is dynamically responding to configuration parameters.

---

## Phase 3: User Story 1 - Filter to Specific Contribution Types via CLI (Priority: P1)

**Goal**: Expose the ability to specify contribution types via a new CLI flag.

### Tests (Write First)
- [x] T006 [P] [US1] Add test cases for `--types` CLI flag parsing and validation in `tests/test_cli.py`
- [x] T007 [P] [US1] Create an integration test in `tests/test_contrib_card.py` to verify the end-to-end flow with the types flag

### Implementation
- [x] T008 [US1] Add `--types` (and `--contrib-types` alias) flag to the `contrib` command in `src/cli.py` with validation against `VALID_CONTRIB_TYPES`

**Checkpoint**: Users can successfully filter their contributor card via the local CLI.

---

## Phase 4: User Story 2 - Filter Contributions via Automation (Priority: P1)

**Goal**: Allow configuration of contribution types via GitHub Actions inputs.

### Implementation
- [x] T009 [US2] Add `contrib_types` input parameter to `action.yml`, mapped to the CLI `--types` flag
- [x] T010 [US2] Document the new `contrib_types` parameter in the `README.md` usage examples

**Checkpoint**: GitHub Actions workflows can utilize the new filtering logic.

---

## Phase 5: Polish & Quality

**Purpose**: Ensure strict adherence to constitution and project standards

- [x] T011 Run `uv run ruff check src tests` and fix any linting violations
- [x] T012 Run `uv run ruff format src tests` to ensure code formatting consistency
- [x] T013 Run `uv run mypy src` and fix any type checking errors
- [x] T014 Run all tests with `uv run pytest` to ensure no regressions were introduced

## Remediation: Gaps

- [x] T015 [P] Update `action.yml` input description to reflect that the default value is 'commits' in `action.yml` [Sync: Gap Report]

### Revision: Implementation Sync 2026-03-22
- Reason: Reconciled documentation and code to ensure the default value for the `--types` flag is strictly 'commits' instead of all four contribution types.

---

## Implementation Strategy
- **MVP**: Complete Phase 1 through Phase 3 to establish local CLI functionality.
- **Dependencies**: Phase 2 depends on Phase 1. Phase 3 depends on Phase 2. Phase 4 depends on Phase 3.
- **Parallel Execution**: Within Phase 3, tests (T006, T007) can be developed in parallel with the foundational CLI implementation (T008) utilizing mocking before the full integration is wired up.