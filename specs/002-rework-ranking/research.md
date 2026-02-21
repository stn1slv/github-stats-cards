# Research: Rework Ranking Calculation

**Feature**: Rework Ranking Calculation
**Status**: Completed

## 1. Project Magnitude Logic (Revised)

**Requirement**: Calculate rank modifier based on "Project Magnitude" rather than individual contribution intensity.
**Decision**: Use **Repository Total Commits** as the proxy for magnitude. This ensures that contributing to large, established projects (like Debezium or Linux) highlights the impact of the contribution, regardless of the user's total commits to that specific repo.

**Implementation**: 
- The GraphQL query `object(expression: "HEAD") { ... on Commit { history { totalCount } } }` is added to all four contribution blocks (Commits, PRs, Issues, Reviews).
- This ensures magnitude is captured even if the user hasn't made any commits to the repository.

## 2. Rank Thresholds & Modifiers (Final)

**Star Thresholds (Base Rank)**:
- **S**: > 10,000 stars
- **A**: 1,001 - 10,000 stars
- **B**: 101 - 1,000 stars
- **C**: 11 - 100 stars
- **D**: 0 - 10 stars

**Modifier Thresholds (Project Magnitude)**:
- **High (+)**: > 5,000 total commits (proxy for Large/Mature projects).
- **Low (-)**: 1 - 99 total commits (proxy for Small/New projects).
- **Neutral**: 100 - 5,000 commits OR Unknown magnitude (0 commits fetched).

**Rationale**: Treating 0 as Neutral prevents unfair downgrades when the default branch is inaccessible or magnitude data is unavailable.

## 3. Visual Rendering

**Requirement**: Auto-scale font size for multi-character ranks (e.g., "A+").
**Implementation**:
- `src/rendering/contrib.py` dynamically sets `font-size: 8px` if `len(rank) > 1`, otherwise `10px`.
- This ensures the rank fits within the existing visual circle without breaking alignment.

## 4. API & Data Model

**Function Signature**:
- `calculate_repo_rank(stars: int, total_repo_commits: int) -> str`

**Logic Flow**:
1. `fetch_contributor_stats` fetches repositories over the last 5 years.
2. For each repository, it extracts `total_repo_commits` from the commit history.
3. It aggregates contributions (Commits, PRs, Issues, Reviews) for sorting.
4. It calculates the rank using `calculate_repo_rank(stars, total_repo_commits)`.
5. The rank is assigned to `rank_level` and rendered in the SVG.
