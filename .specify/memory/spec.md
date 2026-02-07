# Project Specification: GitHub Stats Card

## Overview
A Python CLI tool that generates beautiful GitHub stats cards as SVG images for your profile README. It fetches data from GitHub's GraphQL and REST APIs and renders them locally using customizable themes.

## User Stories
- **US-001:** As a GitHub user, I want to display my repository statistics (stars, commits, PRs, etc.) on my profile in a visually appealing way.
- **US-002:** As a developer, I want to showcase my most used programming languages to highlight my expertise.
- **US-003:** As a user, I want to customize the look of my stats cards with themes and custom colors to match my profile aesthetic.
- **US-004:** As a GitHub Actions user, I want to automate the generation of these cards daily/weekly.
- **US-005:** As an international user, I want the stats cards to support my local language.

## Functional Requirements

### Core System
- **FR-001: Data Fetching**
  - Fetch user statistics (stars, commits, PRs, issues, reviews, contributions) using GitHub GraphQL API.
  - Fetch language usage data from repositories with configurable weighting (size vs. count).
  - Support Personal Access Token (PAT) for authentication.
- **FR-002: CLI Interface**
  - Provide a CLI with subcommands for each card type (`stats`, `top-langs`).
  - Support global flags for customization (themes, colors, output path).
- **FR-003: Internationalization**
  - Support multiple locales for stat labels (e.g., "Stars" -> "Étoiles").
- **FR-004: GitHub Enterprise Support**
  - Support custom GitHub API and GraphQL endpoints via environment variables.

### Card Type: Stats Card
- **FR-005: Stats Calculation**
  - Aggregate total commits, PRs (total/merged), issues, reviews, and stars.
  - **Ranking System:** Calculate a user rank (S+, S, A, B, etc.) using a percentile-based algorithm based on weighted contributions.
- **FR-006: Stats Rendering**
  - Render a vertical list of statistics with optional icons.
  - Display the calculated rank in a dedicated visual circle.
  - Allow hiding specific stats or the rank circle.

### Card Type: Top Languages Card
- **FR-007: Language Aggregation**
  - Aggregate language usage across all public repositories.
  - **Weighting:** Support "Size-Only", "Balanced" (70/30), "Expertise" (50/50), and "Diversity" (40/60) weighting strategies for ranking languages.
  - Exclude specific repositories or languages via CLI flags.
- **FR-008: Language Rendering**
  - Support 5 distinct layouts:
    1. **Normal:** Vertical list with progress bars.
    2. **Compact:** Horizontal stacked bar with legend (matches Stats Card width).
    3. **Donut:** Circular chart with legend.
    4. **Donut-Vertical:** Circular chart with vertical legend.
    5. **Pie:** Pie chart with legend.
  - Display percentage or byte count.

## Non-Functional Requirements
- **NFR-001: Performance** - Card generation should be fast (fetching data is the bottleneck).
- **NFR-002: Reliability** - Handle API errors and rate limiting gracefully.
- **NFR-003: Extensibility** - Easy to add new card types, themes, or layouts.

## Key Entities

### StatsCardConfig
Configuration for stats card rendering:
- `theme`, `colors` (title, text, icon, bg, border, ring)
- `hide`, `show` (specific stats)
- `hide_rank`, `show_icons`
- `include_all_commits`

### LangsCardConfig
Configuration for top languages card rendering:
- `layout` (normal, compact, donut, etc.)
- `langs_count` (max languages to show)
- `weighting` (size vs count weights)
- `stats_format` (percentages vs bytes)

### UserStats (Data Model)
TypedDict containing:
- `totalStars`, `totalCommits`, `totalPRs`, `totalIssues`, `totalReviews`
- `contributedTo`, `mergedPRs`
- `rank` (calculated)

### Language (Data Model)
Dataclass containing:
- `name`
- `color` (Hex)
- `size` (Bytes)
- `count` (Repositories using it)

## Architecture

### Data Flow by Card Type

**1. Stats Card Flow:**
`cli.stats` -> `fetcher.fetch_stats` (GraphQL) -> `rank.calculate_rank` -> `stats_card.render_stats_card` -> `card.render_card` (Base SVG) -> Output File

**2. Top Languages Card Flow:**
`cli.top_langs` -> `langs_fetcher.fetch_top_languages` (GraphQL/REST) -> `langs_card.trim_top_languages` -> `langs_card.render_top_languages` (Layout Selection) -> `card.render_card` (Base SVG) -> Output File

### Layered Architecture
- **Entry Point:** `src/cli.py` (Click-based CLI)
- **Data Layer:** `src/fetcher.py`, `src/langs_fetcher.py` (GitHub API clients)
- **Logic Layer:**
  - `src/rank.py` (Ranking algorithm for Stats)
  - `src/langs_card.py` (Trimming/Sorting logic for Langs)
- **Presentation Layer:**
  - `src/card.py` (Base SVG template & CSS)
  - `src/stats_card.py` (Stats-specific composition)
  - `src/langs_card.py` (Language-specific composition & layouts)
- **Utilities:** `src/colors.py`, `src/utils.py`, `src/i18n.py`

## Edge Cases and Error Handling
- Invalid GitHub Token (401 Unauthorized)
- User Not Found (404 Not Found)
- GitHub API Rate Limiting
- Missing Language Colors (fallback to default)
- Repositories with no languages
