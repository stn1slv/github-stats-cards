"""Command-line interface for GitHub Stats Card generator."""

import os
import sys
from typing import Union

import click

from .fetcher import FetchError, fetch_stats
from .stats_card import render_stats_card


@click.command()
@click.option(
    "--username",
    "-u",
    required=True,
    help="GitHub username",
)
@click.option(
    "--token",
    "-t",
    envvar="GITHUB_TOKEN",
    required=True,
    help="GitHub Personal Access Token (or set GITHUB_TOKEN env var)",
)
@click.option(
    "--output",
    "-o",
    required=True,
    type=click.Path(),
    help="Output SVG file path",
)
@click.option(
    "--theme",
    default="default",
    help="Theme name (default, dark, radical, etc.)",
)
@click.option(
    "--show-icons",
    is_flag=True,
    help="Show icons next to stats",
)
@click.option(
    "--hide-border",
    is_flag=True,
    help="Hide card border",
)
@click.option(
    "--hide-title",
    is_flag=True,
    help="Hide card title",
)
@click.option(
    "--hide-rank",
    is_flag=True,
    help="Hide rank circle",
)
@click.option(
    "--include-all-commits",
    is_flag=True,
    help="Count all commits (not just current year)",
)
@click.option(
    "--commits-year",
    type=int,
    help="Filter commits to specific year (e.g., 2023)",
)
@click.option(
    "--hide",
    default="",
    help="Comma-separated stats to hide (e.g., stars,prs)",
)
@click.option(
    "--show",
    default="",
    help="Comma-separated additional stats to show (e.g., reviews,discussions_started)",
)
@click.option(
    "--title-color",
    help="Custom title color (hex without #)",
)
@click.option(
    "--text-color",
    help="Custom text color (hex without #)",
)
@click.option(
    "--icon-color",
    help="Custom icon color (hex without #)",
)
@click.option(
    "--bg-color",
    help="Custom background color (hex without # or gradient: angle,color1,color2)",
)
@click.option(
    "--border-color",
    help="Custom border color (hex without #)",
)
@click.option(
    "--ring-color",
    help="Custom rank ring color (hex without #)",
)
@click.option(
    "--custom-title",
    help="Custom card title text",
)
@click.option(
    "--locale",
    default="en",
    help="Language locale (default: en)",
)
@click.option(
    "--card-width",
    type=int,
    help="Card width in pixels",
)
@click.option(
    "--line-height",
    type=int,
    default=25,
    help="Line height between stats (default: 25)",
)
@click.option(
    "--border-radius",
    type=float,
    default=4.5,
    help="Border radius (default: 4.5)",
)
@click.option(
    "--number-format",
    type=click.Choice(["short", "long"]),
    default="short",
    help="Number format: short (6.6k) or long (6626)",
)
@click.option(
    "--number-precision",
    type=int,
    help="Decimal places for short format (0-2)",
)
@click.option(
    "--rank-icon",
    type=click.Choice(["default", "github", "percentile"]),
    default="default",
    help="Rank icon style",
)
@click.option(
    "--disable-animations",
    is_flag=True,
    help="Disable CSS animations",
)
@click.option(
    "--text-bold/--no-text-bold",
    default=True,
    help="Use bold text (default: yes)",
)
def main(
    username: str,
    token: str,
    output: str,
    theme: str,
    show_icons: bool,
    hide_border: bool,
    hide_title: bool,
    hide_rank: bool,
    include_all_commits: bool,
    commits_year: Union[int, None],
    hide: str,
    show: str,
    title_color: Union[str, None],
    text_color: Union[str, None],
    icon_color: Union[str, None],
    bg_color: Union[str, None],
    border_color: Union[str, None],
    ring_color: Union[str, None],
    custom_title: Union[str, None],
    locale: str,
    card_width: Union[int, None],
    line_height: int,
    border_radius: float,
    number_format: str,
    number_precision: Union[int, None],
    rank_icon: str,
    disable_animations: bool,
    text_bold: bool,
) -> None:
    """
    Generate GitHub Stats Card SVG.
    
    This tool fetches your GitHub statistics and generates a beautiful
    SVG card that you can embed in your README.md or profile.
    
    Examples:
    
      # Basic usage with environment variable
      export GITHUB_TOKEN=ghp_xxxxx
      github-stats-card -u octocat -o stats.svg
      
      # With theme and custom options
      github-stats-card -u octocat -o stats.svg --theme vue-dark \\
        --show-icons --hide-border --include-all-commits
      
      # Hide specific stats
      github-stats-card -u octocat -o stats.svg --hide stars,prs
      
      # Show additional stats
      github-stats-card -u octocat -o stats.svg --show reviews,discussions_started
    """
    try:
        # Parse hide/show lists
        hide_list = [s.strip() for s in hide.split(",") if s.strip()]
        show_list = [s.strip() for s in show.split(",") if s.strip()]

        # Fetch stats from GitHub
        click.echo(f"Fetching GitHub stats for {username}...", err=True)
        stats = fetch_stats(
            username=username,
            token=token,
            include_all_commits=include_all_commits,
            commits_year=commits_year,
            show=show_list,
        )

        click.echo(f"Found stats for {stats['name']} (@{stats['login']})", err=True)

        # Render SVG card
        click.echo("Generating SVG card...", err=True)
        svg = render_stats_card(
            stats=stats,
            theme=theme,
            hide=hide_list,
            show=show_list,
            hide_title=hide_title,
            hide_border=hide_border,
            hide_rank=hide_rank,
            show_icons=show_icons,
            title_color=title_color,
            text_color=text_color,
            icon_color=icon_color,
            bg_color=bg_color,
            border_color=border_color,
            ring_color=ring_color,
            custom_title=custom_title,
            locale=locale,
            card_width=card_width,
            line_height=line_height,
            border_radius=border_radius,
            number_format=number_format,
            number_precision=number_precision,
            rank_icon=rank_icon,
            disable_animations=disable_animations,
            text_bold=text_bold,
            include_all_commits=include_all_commits,
        )

        # Write to file
        output_path = os.path.abspath(output)
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg)

        click.echo(f"✅ Generated {output_path}", err=True)

    except FetchError as e:
        click.echo(f"❌ Error fetching data: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
