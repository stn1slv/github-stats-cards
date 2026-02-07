# Data Model: Add contributor card

**Feature**: `001-contributor-card` | **Date**: 2026-02-07

## Configuration Model

### `ContribCardConfig`
**Location**: `src/core/config.py`
**Inherits**: `BaseConfig`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `limit` | `int` | `10` | Max number of repositories to display. |
| `exclude_repos` | `set[str]` | `set()` | Repositories to exclude (format: "owner/repo"). |
| `theme` | `str` | `"default"` | Visual theme name. |
| `title_color` | `str \| None` | `None` | Override title color. |
| `text_color` | `str \| None` | `None` | Override text color. |
| `bg_color` | `str \| None` | `None` | Override background color. |
| `border_color` | `str \| None` | `None` | Override border color. |
| `hide_border` | `bool` | `False` | Toggle border visibility. |
| `card_width` | `int` | `467` | Card width in pixels. |
| `disable_animations` | `bool` | `False` | Disable CSS animations. |

### `ContribFetchConfig`
**Location**: `src/core/config.py`
**Inherits**: `BaseConfig`

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `username` | `str` | - | Target GitHub username. |
| `token` | `str` | - | GitHub PAT. |
| `limit` | `int` | `10` | Fetch limit (used to optimize query). |
| `exclude_repos` | `set[str]` | `set()` | Filter set. |

## Domain Entities

### `ContributorRepo`
**Location**: `src/github/fetcher.py` (TypedDict)

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Full name ("owner/repo"). |
| `stars` | `int` | Stargazer count. |
| `avatar_b64` | `str` | Base64 encoded avatar image (data URI). |

### `ContributorStats`
**Location**: `src/github/fetcher.py` (TypedDict)

| Field | Type | Description |
|-------|------|-------------|
| `repos` | `list[ContributorRepo]` | Sorted list of contributed repositories. |

## API Contracts

### Fetcher Interface
`src/github/fetcher.py`

```python
def fetch_contributor_stats(
    config: ContribFetchConfig
) -> ContributorStats:
    """
    Fetches contribution data, sorts by stars, and embeds avatars.
    
    1. Query GraphQL for `repositoriesContributedTo` (first 100).
    2. Filter out user-owned repos.
    3. Filter out `config.exclude_repos`.
    4. Sort by stars descending.
    5. Slice top `config.limit`.
    6. Fetch and base64 encode avatars for the slice.
    """
```

### Renderer Interface
`src/rendering/contrib.py`

```python
def render_contrib_card(
    stats: ContributorStats,
    config: ContribCardConfig
) -> str:
    """
    Renders the SVG card.
    
    1. Initialize SVG with `config.card_width` and dynamic height.
    2. Render header ("Top Contributions").
    3. Iterate `stats.repos`:
       - Render row with avatar (circular clipPath), name, and star count.
    4. Return full SVG string.
    """
```
