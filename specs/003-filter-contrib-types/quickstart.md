# Quickstart: Filter Contribution Types

## Local CLI

To generate a Contributor Card that includes your repository commits and merged/open pull requests (this is the **default behavior**), you don't need any additional flags.

If you want to filter further (e.g., only commits) or expand the list, use the `--types` (or `--contrib-types`) flag:

```bash
# Explicitly requesting only commits
uv run github-stats-card contrib -u your_username --types commits -o contrib.svg

# Requesting all types including issues and reviews
uv run github-stats-card contrib -u your_username --types commits,prs,issues,reviews -o contrib.svg
```

### Allowed Values
The `--types` flag accepts a comma-separated list of the following values:
*   `commits`
*   `prs`
*   `issues`
*   `reviews`

By default, if the flag is omitted, `commits` and `prs` are included.

## GitHub Actions

You can configure the filtering in your GitHub Actions workflow by adding the `contrib_types` parameter to the `with` block:

```yaml
steps:
  - uses: actions/checkout@v4
  - name: Generate GitHub Stats
    uses: ./ # or your action reference
    with:
      token: ${{ secrets.GITHUB_TOKEN }}
      username: your_username
      contrib_types: 'commits,prs'
```