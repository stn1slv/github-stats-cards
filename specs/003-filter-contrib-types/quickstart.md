# Quickstart: Filter Contribution Types

## Local CLI

To generate a Contributor Card that only includes your code commits and pull requests (excluding issues and code reviews), use the `--types` (or `--contrib-types`) flag:

```bash
uv run github-stats-card contrib -u your_username --types commits,prs -o contrib.svg
```

### Allowed Values
The `--types` flag accepts a comma-separated list of the following values:
*   `commits`
*   `prs`
*   `issues`
*   `reviews`

By default, if the flag is omitted, only `commits` are included.

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