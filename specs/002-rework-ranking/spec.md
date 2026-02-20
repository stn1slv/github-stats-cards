# Feature Specification: Rework Ranking Calculation

**Feature Branch**: `002-rework-ranking`
**Created**: 2026-02-20
**Status**: Draft
**Input**: User description: "I want to rework ranking (S, A, B, ...) calculation for stats (user stats) and contrib (top contribution). I want to use existing ranking for stats only. For contrib, I want to mostly focus on github stars (as a first factor) and commits (as a second factor). For example, https://github.com/debezium/debezium should have 'S' rank."

## Clarifications

### Session 2026-02-20
- Q: Influence of Commit Counts → A: **Modifiers**: Star count sets the base letter (e.g., A); high commit count adds `+`, low adds `-` (e.g., A+).
- Q: Contribution Types for Ranking → A: **Inclusive**: Use "Total Contributions" (commits + PRs + issues) as the modifier instead of just commits.
- Q: Modifier Thresholds → A: **Time-based**: Average contributions per month (or year) active in the repo determines the modifier (e.g., >2/month = `+`).
- Q: Rank Display Format → A: **Auto-scale**: Reduce font size for 2-character ranks (A+, S-) to fit in the circle.
- Q: Months Active Calculation → A: **Distinct Active Months**: Count only months with >0 contributions. (Rate = Total / Distinct Months)

## User Scenarios & Testing

### User Story 1 - Generate Contributor Card with Repository-Specific Ranking (Priority: P1)

As a user, I want the contributor card to assign a rank (S, A, B, etc.) to each repository based on its popularity (stars) and my contribution (commits), so that I can highlight my impact on significant projects.

**Why this priority**: The current implementation incorrectly assigns the user's global rank to every repository, failing to distinguish between contributions to major projects vs. smaller ones.

**Independent Test**:
- Command: `uv run github-stats-card contrib --username [user]`

**Acceptance Scenarios**:

1. **Given** a user has contributed to a highly popular repository (e.g., >5000 stars), **When** generating the contributor card, **Then** that repository is displayed with an 'S' rank.
2. **Given** a user has contributed to a moderately popular repository (e.g., 500 stars), **When** generating the contributor card, **Then** that repository is displayed with an appropriate mid-tier rank (e.g., 'A' or 'B').
3. **Given** two repositories with similar star counts, **When** ranked, **Then** the one with significantly more user commits is ranked higher (or within the same tier if fine-grained ranking is applied).

### User Story 2 - Maintain Legacy Ranking for Stats Card (Priority: P1)

As a user, I want my main stats card to continue using the existing ranking algorithm, so that my overall profile score remains consistent with historical data.

**Why this priority**: Explicit requirement to preserve existing behavior for the main stats card.

**Independent Test**:
- Command: `uv run github-stats-card stats --username [user]`

**Acceptance Scenarios**:

1. **Given** a user's profile stats, **When** generating the stats card, **Then** the global rank displayed matches the output of the legacy algorithm (based on total commits, PRs, issues, reviews, followers).

## Requirements

### CLI Interface Design
- **Command**: `github-stats-card contrib`
- **New Flags/Options**: None. (The change applies to the default logic of the `contrib` command).

### Configuration Changes
- **Dataclass**: `ContribCardConfig`
- **New Fields**: None required, unless tuning thresholds via config is desired (not explicitly requested, so assuming hardcoded defaults for now).

### Functional Requirements

#### Contrib Card Ranking Logic
- **FR-001**: The system MUST calculate a unique rank for each repository listed in the contributor card.
- **FR-002**: The rank calculation MUST prioritize the repository's **Star Count** as the primary factor, determining the base letter (S, A, B, C, D).
- **FR-003**: The rank calculation MUST use the user's **Contribution Rate** (Total Contributions / Distinct Active Months) to that repository as a modifier (adding `+` or `-`) to the base rank.
- **FR-004**: The ranking tiers SHOULD follow a standard distribution based on star count thresholds:
    - **S Tier**: > 10000 Stars (Example: `debezium/debezium` with >12k stars)
    - **A Tier**: > 1000 Stars
    - **B Tier**: > 100 Stars
    - **C Tier**: > 10 Stars
    - **D Tier**: > 1 Stars
- **FR-005**: The system MUST NOT apply the user's global rank to individual repositories in the `contrib` card.

#### Stats Card Ranking Logic
- **FR-006**: The system MUST continue to use the existing `calculate_rank` function (or equivalent logic) for the `stats` command, ensuring no change in output for the main stats card.

### Visual/Output Requirements
- **VR-001**: The Contributor Card SVG MUST display the specific rank (S, A, B...) next to each repository, replacing the currently duplicated global rank.
- **VR-002**: The displayed rank MUST fit within the existing rank circle, with the font size automatically scaled down if necessary to accommodate multi-character ranks (e.g., A+).

## Success Criteria

### Measurable Outcomes
- **SC-001**: `contrib` command output shows distinct ranks for different repositories based on their star counts (e.g., a mix of S, A, B depending on the repo list).
- **SC-002**: `stats` command output remains bitwise identical (or semantically identical regarding rank) to the previous version.
- **SC-003**: Unit tests verify that a repo with high stars (e.g., 10,000) and user commits gets an 'S' rank.
