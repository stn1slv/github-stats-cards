# Feature Specification: Filter Contribution Types for Contributor Card

**Feature Branch**: `003-filter-contrib-types`  
**Created**: 2026-03-22  
**Status**: Draft  
**Input**: User description: "Here is the updated feature request, including the requirement for it to be configurable via GitHub Actions: *** ### Title: Feature Request: Add optional flag to filter contribution types for Contributor Card **Is your feature request related to a problem? Please describe.** Currently, the `contrib` card automatically fetches and aggregates data across all four available GitHub contribution types: Commits, Pull Requests, Issues, and Code Reviews. While this provides a great overview, some users might want to highlight specific types of contributions. For example, a user might only want to showcase repositories where they have contributed actual code (Commits/PRs) rather than repositories where they have only opened issues or done reviews. **Describe the solution you'd like** I would like an optional configuration parameter added to the Contributor Card to specify exactly which types of contributions should be taken into account when fetching and ranking repositories. This needs to be available both in the local CLI and when running the tool via GitHub Actions. The supported types should map to the GitHub GraphQL API: 1. `commits` (`commitContributionsByRepository`) 2. `prs` (`pullRequestContributionsByRepository`) 3. `issues` (`issueContributionsByRepository`) 4. `reviews` (`pullRequestReviewContributionsByRepository`) **Proposed Implementation Details:** 1. **CLI Flag**: Add a `--types` or `--contrib-types` flag to the `contrib` command that accepts a comma-separated list of types. *Example:* `uv run github-stats-card contrib -u <username> --types commits,prs` 2. **GitHub Actions Input**: Add a new input parameter (e.g., `contrib_types`) to `action.yml` so users can configure this behavior in their CI/CD workflows. *Example yaml:* ```yaml with: contrib_types: 'commits,prs' ``` 3. **Configuration (`ContribFetchConfig`)**: Add a new parameter `contribution_types: list[str]` which defaults to all four types (`["commits", "prs", "issues", "reviews"]`) to maintain backward compatibility. 4. **Fetching Logic (`src/github/fetcher.py`)**: Update `_async_process_year_contributions` to conditionally include or skip the GraphQL queries for the contribution types based on the provided configuration. **Describe alternatives you've considered** Currently, the only way to filter out certain repositories is by using the `--exclude-repo` flag, but this is a manual, repository-by-repository approach rather than a behavior-based filter. **Additional context** Default behavior should remain unchanged (all types enabled). By allowing users to opt-in to specific contribution types, the tool becomes much more flexible for different types of profiles (e.g., highlighting open-source code contributions vs. community management/issue triage) across both local generation and automated profile README updates."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Filter to Specific Contribution Types via CLI (Priority: P1)

As a user generating a contributor card via the CLI, I want to specify which types of contributions to consider (e.g., only commits and pull requests) so that my generated card highlights only my active code contributions rather than code reviews or issues.

**Why this priority**: Filtering contribution types is the core feature requested to allow users to showcase specific kinds of work.

**Independent Test**: Verify the generated output only includes repositories where the user has the specified contribution types.
- Example Command: `uv run github-stats-card contrib -u <username> --types commits,prs -o contrib.svg`

**Acceptance Scenarios**:

1. **Given** a valid username, **When** `uv run github-stats-card contrib -u <username> --types commits,prs`, **Then** the file is generated, and the underlying data fetch only queries for commits and pull requests.
2. **Given** an invalid type in the types flag, **When** `uv run github-stats-card contrib -u <username> --types invalid`, **Then** the CLI should fail with an appropriate error message indicating invalid contribution types.

---

### User Story 2 - Filter Contributions via Automation (Priority: P1)

As a user running the stats card generation in an automated workflow (e.g., GitHub Actions), I want to configure the contribution types via inputs so that my profile is automatically updated with my filtered contribution data.

**Why this priority**: Automation support was explicitly requested and is the primary way many users generate these cards for their profiles.

**Independent Test**: Verify the workflow definition accepts the new input and passes it correctly.

**Acceptance Scenarios**:

1. **Given** an automated workflow specifying `contrib_types: 'commits,prs'`, **When** the workflow runs, **Then** the internal generation call includes the correct filter.

## Requirements *(mandatory)*

### CLI Interface Design
- **Command**: `github-stats-card contrib`
- **New Flags/Options**:
  - `--types`: Comma-separated list of contribution types to include. Allowed values: `commits`, `prs`, `issues`, `reviews`. (Default: `commits,prs,issues,reviews`)

### Configuration Changes
- **Dataclass**: `ContribFetchConfig`
- **New Fields**:
  - `contribution_types: list[str]` - Types of contributions to fetch

### Functional Requirements
- **FR-001**: System MUST parse the comma-separated `--types` flag into a list, validating against the allowed values (`commits`, `prs`, `issues`, `reviews`).
- **FR-002**: System MUST default to including all 4 contribution types if the flag is omitted, preserving backwards compatibility.
- **FR-003**: System MUST update the data fetching process to only request data for the specified contribution types, ignoring the others.
- **FR-004**: System MUST expose a new `contrib_types` input parameter in the automation definition (`action.yml`).

### Visual/Output Requirements
- **VR-001**: The rendered image MUST NOT change its visual layout; only the underlying data populating the repositories will change based on the filter.

### Assumptions & Dependencies
- **Assumptions**: The available contribution types from the provider API remain consistent (`commits`, `prs`, `issues`, `reviews`).
- **Dependencies**: The automation workflow (`action.yml`) maps directly to the CLI options.

## Success Criteria *(mandatory)*

### Measurable Outcomes
- **SC-001**: Users can successfully limit fetched repositories to those matching specific contribution types without the visual layout breaking.
- **SC-002**: The automation workflow successfully accepts the new configuration parameter and passes it to the generation process.
- **SC-003**: Omitting the new configuration retains the exact previous behavior (fetching all 4 types).
- **SC-004**: Providing an invalid type results in a clear validation error before any data fetching begins.
