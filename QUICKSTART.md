# Quick Start Guide

Get your GitHub stats card up and running in 5 minutes!

## 1. Installation (1 min)

```bash
# Clone or navigate to the project
cd github-stats-card

# Create virtual environment and install
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

## 2. Get GitHub Token (2 min)

1. Go to https://github.com/settings/tokens/new
2. Give it a name: "GitHub Stats Card"
3. Select scopes: `read:user` (public repos only)
4. Click "Generate token"
5. Copy the token (starts with `ghp_`)

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

## 3. Generate Your Card (1 min)

```bash
# Replace 'yourusername' with your GitHub username
github-stats-card -u yourusername -o my-stats.svg
```

That's it! You now have `my-stats.svg` in your current directory.

## 4. Embed in README (1 min)

Add this to your README.md:

```markdown
![My GitHub Stats](my-stats.svg)
```

Commit and push:

```bash
git add my-stats.svg README.md
git commit -m "Add GitHub stats card"
git push
```

## Popular Presets

### Minimal Dark

```bash
github-stats-card -u yourusername -o stats.svg \
  --theme vue-dark \
  --hide-border \
  --hide-title
```

### Colorful with Icons

```bash
github-stats-card -u yourusername -o stats.svg \
  --theme radical \
  --show-icons
```

### Professional Light

```bash
github-stats-card -u yourusername -o stats.svg \
  --theme default \
  --show-icons \
  --include-all-commits
```

## Automation with GitHub Actions

Create `.github/workflows/stats.yml`:

```yaml
name: Stats

on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.13'
      - run: pip install uv
      - run: uv pip install --system -e .
      - env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          github-stats-card -u ${{ github.repository_owner }} -o stats.svg \
            --theme vue-dark --show-icons --hide-border
      - run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add stats.svg
          git diff --quiet || git commit -m "Update stats"
          git push
```

Done! Your stats will update daily automatically.

## Programmatic Usage (Python API)

If you want to use this tool in your Python scripts:

```python
from src.fetcher import fetch_user_stats
from src.stats_card import render_stats_card
from src.config import StatsCardConfig
import os

# Fetch stats
token = os.environ["GITHUB_TOKEN"]
stats = fetch_user_stats(username="yourusername", token=token)

# Configure and render
config = StatsCardConfig(
    theme="vue-dark",
    show_icons=True,
    hide_border=True,
)

svg = render_stats_card(stats, config)

# Save
with open("my-stats.svg", "w") as f:
    f.write(svg)
```

See [EXAMPLES.md](EXAMPLES.md) for more Python API examples.

## Next Steps

- Browse [50+ themes](src/themes.py)
- See [EXAMPLES.md](EXAMPLES.md) for advanced usage
- Read [README.md](README.md) for full documentation
