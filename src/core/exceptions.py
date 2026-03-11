"""Exception hierarchy for GitHub Stats Card."""


class GitHubStatsCardError(Exception):
    """Base exception for all GitHub Stats Card errors."""


class APIError(GitHubStatsCardError):
    """GitHub API request failed."""


class FetchError(APIError):
    """Error fetching data from GitHub API.

    Kept for backwards compatibility. Use APIError for new code.
    """


class LanguageFetchError(APIError):
    """Error fetching language data from GitHub API.

    Kept for backwards compatibility. Use APIError for new code.
    """


class ValidationError(GitHubStatsCardError):
    """Invalid configuration or input parameters."""


class RenderError(GitHubStatsCardError):
    """SVG rendering failed."""


class ThemeError(GitHubStatsCardError):
    """Theme-related error (invalid theme name, missing colors, etc.)."""


class ColorError(ValidationError):
    """Invalid color specification."""
