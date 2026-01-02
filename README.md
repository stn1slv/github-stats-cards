# GitHub Stats Card

A Python CLI tool that generates beautiful GitHub stats cards as SVG images for your profile README.

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-59%20passed-success.svg)](#testing)

## Features

- 🎨 **50+ Built-in Themes** - Choose from a variety of beautiful color schemes
- 📊 **Comprehensive Stats** - Stars, commits, PRs, issues, reviews, and more
- 🔤 **Top Languages Card** - Show your most used programming languages with 5 layouts
- 🔧 **Highly Customizable** - Customize colors, layout, and content
- 🚀 **GitHub Actions Ready** - Perfect for automated daily/weekly updates
- 🎯 **Local Generation** - No external service dependencies
- 🌐 **Internationalization** - Support for multiple languages (English included)

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get started in 5 minutes
- **[Usage Examples](EXAMPLES.md)** - 13+ detailed examples
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute
- **[Project Summary](PROJECT_SUMMARY.md)** - Implementation overview

## Installation

### Using uv (recommended)

```bash
uv pip install -e .
```

### Using pip

```bash
pip install -e .
```

> **Note:** This project uses `uv` for all Python execution, testing, and package management. All examples in this documentation use `uv` commands.

### Running Without Installation

You can run the application directly without installing it using `uv run`:

```bash
# Run as a Python module
uv run python -m src.cli -u your-username -o stats.svg

# Or using the shorter form
uv run python -m src -u your-username -o stats.svg
```

**Important:** Don't forget to set your GitHub token:
```bash
export GITHUB_TOKEN=ghp_your_token_here
uv run python -m src.cli -u your-username -o stats.svg
```

Or pass it directly:
```bash
uv run python -m src.cli -u your-username -o stats.svg --token ghp_your_token_here
```

## Quick Start

### Set up your GitHub token

Create a Personal Access Token (PAT) with `read:user` scope:
https://github.com/settings/tokens/new

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

### Generate your cards

```bash
# GitHub stats card
github-stats-card stats -u your-username -o stats.svg

# Top languages card
github-stats-card top-langs -u your-username -o top-langs.svg
```

## Usage

The CLI provides two main commands:
- `stats` - Generate GitHub stats card
- `top-langs` - Generate top languages card

### GitHub Stats Card

```bash
# Generate with default theme
github-stats-card stats -u octocat -o stats.svg

# Use a specific theme
github-stats-card stats -u octocat -o stats.svg --theme vue-dark

# Show icons and hide border
github-stats-card stats -u octocat -o stats.svg --show-icons --hide-border
```

### Top Languages Card

```bash
# Generate with default layout (normal)
github-stats-card top-langs -u octocat -o top-langs.svg

# Compact layout
github-stats-card top-langs -u octocat -o top-langs.svg --layout compact

# Donut chart with dark theme
github-stats-card top-langs -u octocat -o top-langs.svg \
  --layout donut --theme vue-dark --hide-border

# Hide specific languages
github-stats-card top-langs -u octocat -o top-langs.svg \
  --hide "HTML,CSS,Makefile" --langs-count 8

# Pie chart with bytes display
github-stats-card top-langs -u octocat -o top-langs.svg \
  --layout pie --stats-format bytes
```

### Advanced Options

**Stats Card:**
```bash
# Hide specific stats
github-stats-card stats -u octocat -o stats.svg --hide stars,prs

# Show additional stats
github-stats-card stats -u octocat -o stats.svg --show reviews,discussions_started

# Include all commits (not just current year)
github-stats-card stats -u octocat -o stats.svg --include-all-commits

# Custom colors
github-stats-card stats -u octocat -o stats.svg \
  --title-color ff6e96 \
  --text-color f8f8f2 \
  --bg-color 282a36

# Gradient background
github-stats-card stats -u octocat -o stats.svg \
  --bg-color "90,ff0000,00ff00,0000ff"
```

**Top Languages Card:**
```bash
# Exclude specific repositories
github-stats-card top-langs -u octocat -o top-langs.svg \
  --exclude-repo "repo1,repo2"

# Custom weighting (balance size and repo count)
github-stats-card top-langs -u octocat -o top-langs.svg \
  --size-weight 0.5 --count-weight 0.5

# Custom width and colors
github-stats-card top-langs -u octocat -o top-langs.svg \
  --card-width 400 \
  --title-color ff6e96 \
  --text-color f8f8f2 \
  --bg-color 282a36
```

### All Options

Run `github-stats-card stats --help` or `github-stats-card top-langs --help` for complete option lists.

**Stats Card Options:**
- Basic: username, token, output, theme
- Display: show-icons, hide-border, hide-title, hide-rank, hide/show stats
- Commits: include-all-commits, commits-year
- Colors: title-color, text-color, icon-color, bg-color, border-color, ring-color
- Layout: card-width, line-height, border-radius
- Formatting: number-format, number-precision, locale, custom-title
- Other: rank-icon, disable-animations, text-bold

**Top Languages Card Options:**
- Basic: username, token, output, theme
- Display: hide-border, hide-title, hide-progress
- Layout: layout (normal/compact/donut/donut-vertical/pie), card-width, border-radius
- Languages: langs-count, hide (languages), exclude-repo
- Ranking: size-weight, count-weight
- Colors: title-color, text-color, bg-color, border-color
- Other: stats-format (percentages/bytes), custom-title, disable-animations

## Available Themes

Here are some popular themes:

- `default` - Clean and professional
- `dark` - Dark mode friendly
- `radical` - Bold and colorful
- `vue` / `vue-dark` - Vue.js inspired
- `tokyonight` - Tokyo Night theme
- `dracula` - Dracula theme
- `gruvbox` - Gruvbox theme
- `monokai` - Monokai theme
- `github_dark` - GitHub dark theme
- `nord` - Nord theme
- `catppuccin_mocha` / `catppuccin_latte` - Catppuccin themes

[See all 50+ themes](github_stats_card/themes.py)

## GitHub Actions Integration

Create `.github/workflows/update-stats.yml`:

```yaml
name: Update GitHub Stats

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
  workflow_dispatch:  # Manual trigger

jobs:
  update-stats:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      
      - name: Install uv
        run: pip install uv
      
      - name: Install github-stats-card
        run: uv pip install --system -e .
      
      - name: Generate GitHub Stats Cards
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Stats card - Dark theme
          github-stats-card stats \
            --username ${{ github.repository_owner }} \
            --output img/github-stats-dark.svg \
            --theme vue-dark \
            --show-icons \
            --hide-border \
            --include-all-commits
          
          # Stats card - Light theme
          github-stats-card stats \
            --username ${{ github.repository_owner }} \
            --output img/github-stats-light.svg \
            --theme vue \
            --show-icons \
            --hide-border \
            --include-all-commits
          
          # Top languages card - Dark theme
          github-stats-card top-langs \
            --username ${{ github.repository_owner }} \
            --output img/top-langs-dark.svg \
            --theme vue-dark \
            --layout compact \
            --hide-border \
            --langs-count 8
          
          # Top languages card - Light theme
          github-stats-card top-langs \
            --username ${{ github.repository_owner }} \
            --output img/top-langs-light.svg \
            --theme vue \
            --layout compact \
            --hide-border \
            --langs-count 8
      
      - name: Commit and push if changed
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add img/*.svg
          git diff --staged --quiet || git commit -m "Update GitHub stats [skip ci]"
          git push
```

Then add to your README:

```markdown
## My GitHub Stats

<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="img/github-stats-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="img/github-stats-light.svg">
    <img alt="GitHub Stats" src="img/github-stats-dark.svg">
  </picture>
  
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="img/top-langs-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="img/top-langs-light.svg">
    <img alt="Top Languages" src="img/top-langs-dark.svg">
  </picture>
</div>
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/github-stats-card.git
cd github-stats-card

# Install with dev dependencies
uv pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
# Format code
black github_stats_card tests

# Lint
ruff check github_stats_card tests

# Type check
mypy github_stats_card
```

## Architecture

The project is organized into focused modules:

**Core:**
- `cli.py` - Command-line interface with Click command group
- `card.py` - Base SVG card renderer
- `themes.py` - Theme definitions (50+ themes)
- `colors.py` - Color parsing and utilities
- `utils.py` - Utility functions

**Stats Card:**
- `fetcher.py` - GitHub GraphQL/REST API client for user stats
- `rank.py` - Rank calculation algorithm
- `stats_card.py` - Stats card SVG renderer
- `icons.py` - SVG icon definitions
- `i18n.py` - Internationalization

**Top Languages Card:**
- `langs_fetcher.py` - GitHub GraphQL API client for language stats
- `langs_card.py` - Top languages card SVG renderer (5 layouts)

## Credits

Inspired by [github-readme-stats](https://github.com/anuraghazra/github-readme-stats) by [@anuraghazra](https://github.com/anuraghazra).

This project is a Python CLI reimplementation designed for local generation and GitHub Actions usage.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
