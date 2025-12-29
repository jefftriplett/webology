import time

import typer

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text


ASCII_ART = """
█   █ ███ ███  ██  █   ██   ██  █ █
█ █ █ █   █ █ █  █ █   █ █ █    ▀█▀
█ █ █ ██  ███ █  █ █   █ █ █ ██  █
█▄▀▄█ █   █ █ █  █ █   █ █ █  █  █
▀   ▀ ███ ███  ██  ███ ██   ██   █
"""

CARD_CONTENT = """
Work: Engineer and Partner at REVSYS (https://www.revsys.com)

  Website:  jefftriplett.com
  Links:    webology.dev
  GitHub:   @jefftriplett
  Mastodon: @webology@mastodon.social
  Twitter:  @webology

Projects
  • django-news.com
  • djangopackages.org
  • awesomedjango.org
  • djangocon.us
  • djangojobboard.com

Card: uvx webology
"""

__version__ = "2022.11.2"

RAINBOW_COLORS = [
    "#ff6b6b",
    "#feca57",
    "#48dbfb",
    "#ff9ff3",
    "#54a0ff",
    "#5f27cd",
]


def make_gradient_text(text: str, colors: list[str]) -> Text:
    """Create rainbow gradient text."""
    result = Text()
    lines = text.strip().split("\n")
    for line in lines:
        for i, char in enumerate(line):
            color = colors[i % len(colors)]
            result.append(char, style=color)
        result.append("\n")
    return result


def typing_effect(console: Console, text: Text, panel_title: str, delay: float = 0.01):
    """Display text with a typing animation effect."""
    displayed = Text()
    plain = text.plain

    # Build a map of character index to style
    style_map = {}
    for span in text._spans:
        for i in range(span.start, span.end):
            style_map[i] = span.style

    with Live(Panel(displayed, title=panel_title, border_style="bright_blue"),
              console=console, refresh_per_second=60) as live:
        for i, char in enumerate(plain):
            style = style_map.get(i)
            displayed.append(char, style=style)
            live.update(Panel(displayed, title=panel_title, border_style="bright_blue"))
            if char not in " \n":
                time.sleep(delay)


def main():
    console = Console()

    # Spinner reveal
    with console.status("[bold cyan]Loading card...", spinner="dots"):
        time.sleep(0.8)

    # Create rainbow ASCII art header
    header = make_gradient_text(ASCII_ART, RAINBOW_COLORS)

    # Create the card content
    content = Text()
    content.append(header)
    content.append("\n")

    # Add the rest with some styling
    lines = CARD_CONTENT.strip().split("\n")
    for line in lines:
        if line.startswith("Work:"):
            content.append(line + "\n", style="italic")
        elif line.startswith("Projects"):
            content.append("\n" + line + "\n", style="bold bright_magenta")
        elif line.strip().startswith("•"):
            content.append(line + "\n", style="bright_green")
        elif line.startswith("Card:"):
            content.append("\n" + line + "\n", style="dim italic")
        elif ":" in line and not line.startswith(" "):
            parts = line.split(":", 1)
            content.append(parts[0] + ":", style="bold cyan")
            content.append(parts[1] + "\n", style="white")
        else:
            content.append(line + "\n")

    # Typing animation
    typing_effect(console, content, "[bold]Jeff Triplett[/bold]", delay=0.008)


if __name__ == "__main__":
    typer.run(main)
