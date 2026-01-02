# Example Usage

This guide shows how to use the GitHub Stats Card CLI tool with various options.

## Prerequisites

1. Install the tool:
   ```bash
   uv pip install -e .
   ```

2. Set up your GitHub Personal Access Token:
   ```bash
   export GITHUB_TOKEN=ghp_your_token_here
   ```

## Basic Examples

### 1. Generate a basic stats card

```bash
github-stats-card -u octocat -o stats.svg
```

### 2. Use a dark theme

```bash
github-stats-card -u octocat -o stats.svg --theme dark
```

### 3. Show icons next to stats

```bash
github-stats-card -u octocat -o stats.svg --show-icons
```

### 4. Hide border and title

```bash
github-stats-card -u octocat -o stats.svg --hide-border --hide-title
```

## Advanced Examples

### 5. Multiple theme variants

```bash
# Vue Dark theme
github-stats-card -u octocat -o stats-dark.svg --theme vue-dark --show-icons --hide-border

# Vue Light theme  
github-stats-card -u octocat -o stats-light.svg --theme vue --show-icons --hide-border

# Dracula theme
github-stats-card -u octocat -o stats-dracula.svg --theme dracula --show-icons
```

### 6. Custom colors

```bash
# Custom single colors
github-stats-card -u octocat -o stats.svg \
  --title-color ff6e96 \
  --text-color f8f8f2 \
  --icon-color 79dafa \
  --bg-color 282a36

# Gradient background
github-stats-card -u octocat -o stats.svg \
  --bg-color "90,ff0000,00ff00,0000ff"
```

### 7. Hide specific stats

```bash
# Hide stars and PRs
github-stats-card -u octocat -o stats.svg --hide stars,prs

# Hide multiple stats
github-stats-card -u octocat -o stats.svg --hide stars,commits,prs
```

### 8. Show additional stats

```bash
# Show reviews and discussions
github-stats-card -u octocat -o stats.svg --show reviews,discussions_started

# Show all available stats
github-stats-card -u octocat -o stats.svg \
  --show reviews,discussions_started,discussions_answered,prs_merged
```

### 9. Include all commits (not just current year)

```bash
github-stats-card -u octocat -o stats.svg --include-all-commits
```

### 10. Custom title and styling

```bash
github-stats-card -u octocat -o stats.svg \
  --custom-title "My GitHub Journey" \
  --card-width 500 \
  --line-height 30 \
  --border-radius 10
```

### 11. Number formatting

```bash
# Short format with precision
github-stats-card -u octocat -o stats.svg --number-format short --number-precision 2

# Long format (6626 instead of 6.6k)
github-stats-card -u octocat -o stats.svg --number-format long
```

### 12. Hide rank circle

```bash
github-stats-card -u octocat -o stats.svg --hide-rank
```

### 13. Disable animations

```bash
github-stats-card -u octocat -o stats.svg --disable-animations
```

## Complete Example

Here's a comprehensive example with many options:

```bash
github-stats-card \
  --username octocat \
  --output my-stats.svg \
  --theme tokyonight \
  --show-icons \
  --hide-border \
  --include-all-commits \
  --show reviews,discussions_started \
  --custom-title "GitHub Activity" \
  --card-width 500 \
  --number-format short \
  --number-precision 1
```

## Using with Different Themes

Try different themes to find your favorite:

```bash
# Professional themes
github-stats-card -u octocat -o stats.svg --theme default
github-stats-card -u octocat -o stats.svg --theme graywhite

# Dark themes
github-stats-card -u octocat -o stats.svg --theme dark
github-stats-card -u octocat -o stats.svg --theme tokyonight
github-stats-card -u octocat -o stats.svg --theme dracula
github-stats-card -u octocat -o stats.svg --theme nord
github-stats-card -u octocat -o stats.svg --theme github_dark

# Colorful themes
github-stats-card -u octocat -o stats.svg --theme radical
github-stats-card -u octocat -o stats.svg --theme synthwave
github-stats-card -u octocat -o stats.svg --theme outrun
github-stats-card -u octocat -o stats.svg --theme neon

# Framework-inspired themes
github-stats-card -u octocat -o stats.svg --theme vue
github-stats-card -u octocat -o stats.svg --theme react

# High contrast
github-stats-card -u octocat -o stats.svg --theme highcontrast
```

## Embedding in README

After generating your stats card, add it to your README.md:

```markdown
## My GitHub Stats

![GitHub Stats](stats.svg)

<!-- Or with picture element for theme support -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="stats-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="stats-light.svg">
  <img alt="GitHub Stats" src="stats-dark.svg">
</picture>
```

## Troubleshooting

### Token not found

If you get an error about missing token:

```bash
export GITHUB_TOKEN=ghp_your_token_here
# Or pass it directly
github-stats-card -u octocat -o stats.svg --token ghp_your_token_here
```

### Invalid color

Make sure hex colors don't include the `#` prefix:

```bash
# ✅ Correct
github-stats-card -u octocat -o stats.svg --title-color ff6e96

# ❌ Wrong
github-stats-card -u octocat -o stats.svg --title-color "#ff6e96"
```

### GraphQL errors

If you encounter GraphQL errors, make sure your token has the `read:user` scope.

## Programmatic Usage (Python API)

You can use the library programmatically in your Python projects for custom integrations.

### Basic Stats Card

```python
from src.fetcher import fetch_user_stats
from src.stats_card import render_stats_card
from src.config import StatsCardConfig

# Fetch stats from GitHub
stats = fetch_user_stats(username="octocat", token="ghp_your_token")

# Create configuration
config = StatsCardConfig(
    theme="vue-dark",
    show_icons=True,
    hide_border=True,
)

# Render SVG
svg = render_stats_card(stats, config)

# Save to file
with open("stats.svg", "w") as f:
    f.write(svg)
```

### Advanced Stats Card Configuration

```python
from src.config import StatsCardConfig
from src.stats_card import render_stats_card
from src.fetcher import fetch_user_stats

stats = fetch_user_stats(username="octocat", token="ghp_your_token")

# Custom configuration with all options
config = StatsCardConfig(
    theme="tokyonight",
    show_icons=True,
    hide_border=True,
    hide_title=False,
    hide_rank=False,
    hide=["stars", "prs"],  # Hide specific stats
    show=["reviews", "discussions_started"],  # Show additional stats
    include_all_commits=True,
    custom_title="My GitHub Journey",
    card_width=500,
    line_height=30,
    border_radius=10,
    number_format="short",
    number_precision=1,
    disable_animations=False,
    text_bold=False,
    # Custom colors (overrides theme)
    title_color="ff6e96",
    text_color="f8f8f2",
    icon_color="79dafa",
    bg_color="282a36",
)

svg = render_stats_card(stats, config)
```

### Top Languages Card

```python
from src.langs_fetcher import fetch_top_languages
from src.langs_card import render_top_languages
from src.config import LangsCardConfig

# Fetch language stats
langs = fetch_top_languages(username="octocat", token="ghp_your_token")

# Configure and render
config = LangsCardConfig(
    theme="vue-dark",
    layout="compact",  # normal, compact, donut, donut-vertical, pie
    hide_border=True,
    langs_count=8,
    hide=["HTML", "CSS"],  # Hide specific languages
)

svg = render_top_languages(langs, config)

with open("top-langs.svg", "w") as f:
    f.write(svg)
```

### Different Layouts for Languages Card

```python
from src.config import LangsCardConfig
from src.langs_card import render_top_languages

# Normal layout (horizontal bars)
config_normal = LangsCardConfig(layout="normal", theme="vue-dark")

# Compact layout (vertical list)
config_compact = LangsCardConfig(layout="compact", theme="vue-dark")

# Donut chart
config_donut = LangsCardConfig(layout="donut", theme="vue-dark", hide_border=True)

# Donut vertical (donut with stats beside)
config_donut_v = LangsCardConfig(layout="donut-vertical", theme="vue-dark")

# Pie chart
config_pie = LangsCardConfig(layout="pie", theme="vue-dark", stats_format="bytes")

svg = render_top_languages(langs, config_normal)
```

### Creating Config from CLI-Style Arguments

If you have CLI-style arguments (e.g., from a web form), use `from_cli_args()`:

```python
from src.config import StatsCardConfig, LangsCardConfig

# CLI args are usually strings
cli_args = {
    "theme": "vue-dark",
    "show_icons": True,
    "hide_border": True,
    "hide": "stars,prs",  # comma-separated string
    "show": "reviews,discussions_started",  # comma-separated string
    "custom_title": "My Stats",
}

# Convert to proper config object
config = StatsCardConfig.from_cli_args(**cli_args)

svg = render_stats_card(stats, config)
```

### Batch Generation

```python
from src.fetcher import fetch_user_stats
from src.stats_card import render_stats_card
from src.config import StatsCardConfig

usernames = ["octocat", "torvalds", "gvanrossum"]
token = "ghp_your_token"

for username in usernames:
    stats = fetch_user_stats(username=username, token=token)
    config = StatsCardConfig(theme="vue-dark", show_icons=True)
    svg = render_stats_card(stats, config)
    
    with open(f"{username}-stats.svg", "w") as f:
        f.write(svg)
    
    print(f"Generated stats for {username}")
```

### Custom Integration Example

```python
import os
from src.fetcher import fetch_user_stats
from src.langs_fetcher import fetch_top_languages
from src.stats_card import render_stats_card
from src.langs_card import render_top_languages
from src.config import StatsCardConfig, LangsCardConfig

def generate_github_cards(username: str, output_dir: str = "."):
    """Generate both stats and languages cards for a user."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable required")
    
    # Fetch data
    stats = fetch_user_stats(username=username, token=token)
    langs = fetch_top_languages(username=username, token=token)
    
    # Configure stats card
    stats_config = StatsCardConfig(
        theme="vue-dark",
        show_icons=True,
        hide_border=True,
        include_all_commits=True,
    )
    
    # Configure languages card
    langs_config = LangsCardConfig(
        theme="vue-dark",
        layout="compact",
        hide_border=True,
        langs_count=8,
    )
    
    # Render SVGs
    stats_svg = render_stats_card(stats, stats_config)
    langs_svg = render_top_languages(langs, langs_config)
    
    # Save files
    stats_path = os.path.join(output_dir, f"{username}-stats.svg")
    langs_path = os.path.join(output_dir, f"{username}-langs.svg")
    
    with open(stats_path, "w") as f:
        f.write(stats_svg)
    
    with open(langs_path, "w") as f:
        f.write(langs_svg)
    
    return stats_path, langs_path

# Usage
stats_file, langs_file = generate_github_cards("octocat", output_dir="./img")
print(f"Generated: {stats_file}, {langs_file}")
```

### Error Handling

```python
from src.fetcher import fetch_user_stats
from src.exceptions import APIError, ValidationError

try:
    stats = fetch_user_stats(username="octocat", token="ghp_invalid")
except APIError as e:
    print(f"GitHub API error: {e}")
except ValidationError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Available Configuration Fields

**StatsCardConfig:**
- `theme` (str): Theme name from themes.py
- `show_icons` (bool): Display icons next to stats
- `hide_border` (bool): Hide card border
- `hide_title` (bool): Hide card title
- `hide_rank` (bool): Hide rank circle
- `hide` (list[str]): Stats to hide
- `show` (list[str]): Additional stats to show
- `include_all_commits` (bool): Include commits from all years
- `custom_title` (str | None): Custom card title
- `card_width` (int): Card width in pixels
- `line_height` (int): Line height for stats
- `border_radius` (float): Border radius
- `number_format` (str): "short" or "long"
- `number_precision` (int): Decimal places for short format
- `locale` (str): Language locale
- `disable_animations` (bool): Disable CSS animations
- `text_bold` (bool): Use bold text
- `title_color`, `text_color`, `icon_color`, `bg_color`, `border_color`, `ring_color` (str | None): Custom colors

**LangsCardConfig:**
- `theme` (str): Theme name from themes.py
- `layout` (str): "normal", "compact", "donut", "donut-vertical", "pie"
- `hide_border` (bool): Hide card border
- `hide_title` (bool): Hide card title
- `hide_progress` (bool): Hide progress bars (normal layout)
- `langs_count` (int): Number of languages to show
- `hide` (list[str]): Languages to hide
- `exclude_repo` (list[str]): Repositories to exclude
- `size_weight` (float): Weight for repo size (0-1)
- `count_weight` (float): Weight for repo count (0-1)
- `custom_title` (str | None): Custom card title
- `card_width` (int): Card width in pixels
- `border_radius` (float): Border radius
- `stats_format` (str): "percentages" or "bytes"
- `disable_animations` (bool): Disable CSS animations
- `title_color`, `text_color`, `bg_color`, `border_color` (str | None): Custom colors

