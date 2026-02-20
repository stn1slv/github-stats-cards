# Data Model: Rework Ranking Calculation

**Feature**: Rework Ranking Calculation
**Version**: 1.0.0

## Entities

### `ContributorRepo` (Updated)

Represents a single repository in the contributor card.

```python
class ContributorRepo(TypedDict):
    name: str          # "owner/repo"
    stars: int         # Total stars
    commits: int       # User's commits to this repo
    prs: int           # User's PRs to this repo
    issues: int        # User's issues in this repo
    reviews: int       # User's reviews in this repo
    rank_level: str    # "S", "A+", "B", etc. (Updated logic)
    avatar_b64: str | None
```

### Ranking Function Contract

**Location**: `src/github/rank.py`

```python
def calculate_repo_rank(
    stars: int, 
    total_contribs: int, 
    years_active: int
) -> str:
    """
    Calculate rank for a single repository contribution.
    
    Args:
        stars: Repository star count
        total_contribs: Sum of user's commits, PRs, issues, reviews
        years_active: Count of years with >0 contributions (1-5)
        
    Returns:
        Rank string (e.g., "S", "A+", "B-")
    """
    # Logic:
    # 1. Determine base rank from stars (S > 10k, A > 1k, B > 100, C > 10, D > 1)
    # 2. Calculate annual_rate = total_contribs / max(1, years_active)
    # 3. Apply modifiers:
    #    - Rate >= 50: Append "+"
    #    - Rate < 5: Append "-"
    #    - Otherwise: No modifier
    pass
```

## Configuration

### `ContribCardConfig` (No Change)

No new fields required. The ranking logic is internal.
