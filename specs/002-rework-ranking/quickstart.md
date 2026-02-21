# Quickstart: Rework Ranking Calculation

**Feature**: Rework Ranking Calculation
**Version**: 1.0.0

## Overview

The `contrib` command now calculates ranks for repositories based on their popularity (stars) and your contributions.

## Usage

Generate your top contributor card:

```bash
uv run github-stats-card contrib --username [user]
```

## How It Works

1.  **Star-Based Tiers**: The base rank is determined by the repository's star count.
    *   **S**: > 10,000 Stars (e.g., Debezium)
    *   **A**: 1,001 - 10,000 Stars
    *   **B**: 101 - 1,000 Stars
    *   **C**: 11 - 100 Stars
    *   **D**: 0 - 10 Stars
2.  **Contribution Modifiers**: The rank is adjusted based on the **repository's total commit count** (Project Magnitude).
    *   **+**: Large/Mature Project (> 5,000 commits)
    *   **-**: Small/New Project (1 - 99 commits)
    *   (None): Medium Project (100 - 5,000 commits) OR Unknown Magnitude (0 commits)
3.  **Example**:
    *   Repository: `debezium/debezium` (14k stars, 11k commits) -> **S+** (S Tier + High Magnitude)
    *   Repository: `my-small-repo` (50 stars, 10 commits) -> **C-** (C Tier + Low Magnitude)
    *   Repository: `empty-repo` (100 stars, 0 commits) -> **B** (B Tier + Unknown Magnitude)

## Configuration

No new configuration flags are required. The new ranking logic is automatically applied to all `contrib` cards.
