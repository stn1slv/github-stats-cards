# Research: Rework Ranking Calculation

**Feature**: Rework Ranking Calculation
**Status**: In Progress

## 1. Data Availability for "Contribution Rate"

**Requirement**: Calculate rank modifier based on "Contribution Rate (Total / Distinct Active Months)".
**Current Implementation**: The fetcher iterates through the last 5 years, making one GraphQL query per year to `contributionsCollection`. This yields `totalCount` of contributions per repository for that year.
**Constraint**: GitHub GraphQL API does not provide a "monthly breakdown per repository" in a single query. Getting true "Distinct Active Months" would require querying *each month* individually (5 years * 12 months = 60 queries), which violates performance goals.

**Findings**:
- We can easily track **Distinct Active Years** (count of years where `totalCount > 0` for a repo).
- We cannot efficiently track Distinct Active Months.

**Decision**: 
- Use **Distinct Active Years** as the time unit. 
- Metric: `Annual Contribution Rate = Total Contributions / Distinct Active Years`.
- Thresholds for modifiers (`+`/`-`) will be based on this annual average.

## 2. Rank Thresholds & Modifiers

**Star Thresholds (Base Rank)**:
- **S**: > 10,000
- **A**: > 1,000
- **B**: > 100
- **C**: > 10
- **D**: > 1

**Modifier Thresholds (Annual Rate)**:
- We need empirical defaults.
- **High (+)**: > 50 contributions/year (approx 1/week).
- **Low (-)**: < 5 contributions/year.
- **Neutral**: 5 - 50 contributions/year.

**Implementation**:
- New function `calculate_repo_rank(stars: int, total_contribs: int, active_years: int) -> str` in `src/github/rank.py`.

## 3. Visual Rendering

**Requirement**: Auto-scale font size for 2-character ranks (e.g., "A+").
**Current SVG**:
```xml
<text style="font-size: 10px;">{rank}</text>
```
**Change**:
- If `len(rank) > 1`: Use `font-size: 8px` (or calculated equivalent).
- Center alignment `dominant-baseline="central" text-anchor="middle"` is already used, so changing font size should keep it centered.

## 4. API & Data Model

**Updated `ContributorRepo`**:
No schema change needed in `TypedDict` if we store the full rank string (e.g., "A+") in `rank_level`.

**Logic Flow**:
1. `fetcher.py`:
   - Initialize `repo_years_count = {name: 0}`.
   - Inside the yearly loop, if `count > 0`, increment `repo_years_count[name]`.
   - After loop, calculate rank for each repo using `calculate_repo_rank`.
   - Assign to `rank_level`.
