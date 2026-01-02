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
