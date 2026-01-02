# GitHub Stats Card

A Python CLI tool that generates beautiful GitHub stats cards as SVG images for your profile README.

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-26%20passed-success.svg)](#testing)

## Features

- 🎨 **50+ Built-in Themes** - Choose from a variety of beautiful color schemes
- 📊 **Comprehensive Stats** - Stars, commits, PRs, issues, reviews, and more
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

## Quick Start

### Set up your GitHub token

Create a Personal Access Token (PAT) with `read:user` scope:
https://github.com/settings/tokens/new

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

### Generate your stats card

```bash
github-stats-card -u your-username -o stats.svg
```

## Usage

### Basic Usage

```bash
# Generate with default theme
github-stats-card -u octocat -o stats.svg

# Use a specific theme
github-stats-card -u octocat -o stats.svg --theme vue-dark

# Show icons and hide border
github-stats-card -u octocat -o stats.svg --show-icons --hide-border
```

### Advanced Options

```bash
# Hide specific stats
github-stats-card -u octocat -o stats.svg --hide stars,prs

# Show additional stats
github-stats-card -u octocat -o stats.svg --show reviews,discussions_started

# Include all commits (not just current year)
github-stats-card -u octocat -o stats.svg --include-all-commits

# Custom colors
github-stats-card -u octocat -o stats.svg \
  --title-color ff6e96 \
  --text-color f8f8f2 \
  --bg-color 282a36

# Gradient background
github-stats-card -u octocat -o stats.svg \
  --bg-color "90,ff0000,00ff00,0000ff"
```

### All Options

```
Options:
  -u, --username TEXT             GitHub username [required]
  -t, --token TEXT                GitHub PAT (or set GITHUB_TOKEN) [required]
  -o, --output PATH               Output SVG file path [required]
  --theme TEXT                    Theme name (default, dark, radical, etc.)
  --show-icons                    Show icons next to stats
  --hide-border                   Hide card border
  --hide-title                    Hide card title
  --hide-rank                     Hide rank circle
  --include-all-commits           Count all commits (not just current year)
  --hide TEXT                     Comma-separated stats to hide
  --show TEXT                     Comma-separated additional stats to show
  --title-color TEXT              Custom title color (hex without #)
  --text-color TEXT               Custom text color
  --icon-color TEXT               Custom icon color
  --bg-color TEXT                 Custom background color or gradient
  --border-color TEXT             Custom border color
  --ring-color TEXT               Custom rank ring color
  --custom-title TEXT             Custom card title text
  --locale TEXT                   Language locale (default: en)
  --card-width INTEGER            Card width in pixels
  --line-height INTEGER           Line height between stats (default: 25)
  --border-radius FLOAT           Border radius (default: 4.5)
  --number-format [short|long]    Number format: short (6.6k) or long (6626)
  --number-precision INTEGER      Decimal places for short format (0-2)
  --rank-icon [default|github|percentile]  Rank icon style
  --disable-animations            Disable CSS animations
  --text-bold / --no-text-bold    Use bold text (default: yes)
  --help                          Show this message and exit
```

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
          # Dark theme
          github-stats-card \
            --username ${{ github.repository_owner }} \
            --output img/github-stats-dark.svg \
            --theme vue-dark \
            --show-icons \
            --hide-border \
            --include-all-commits
          
          # Light theme
          github-stats-card \
            --username ${{ github.repository_owner }} \
            --output img/github-stats-light.svg \
            --theme vue \
            --show-icons \
            --hide-border \
            --include-all-commits
      
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

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="img/github-stats-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="img/github-stats-light.svg">
  <img alt="GitHub Stats" src="img/github-stats-dark.svg">
</picture>
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

- `fetcher.py` - GitHub GraphQL/REST API client
- `rank.py` - Rank calculation algorithm
- `stats_card.py` - Stats card SVG renderer
- `card.py` - Base SVG card renderer
- `themes.py` - Theme definitions
- `colors.py` - Color parsing and utilities
- `icons.py` - SVG icon definitions
- `i18n.py` - Internationalization
- `utils.py` - Utility functions
- `cli.py` - Command-line interface

## Credits

Inspired by [github-readme-stats](https://github.com/anuraghazra/github-readme-stats) by [@anuraghazra](https://github.com/anuraghazra).

This project is a Python CLI reimplementation designed for local generation and GitHub Actions usage.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
