import select
import sys
import termios
import time
import tty

import typer

from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text


ASCII_ART = """
█   █ ███ ███  ██  █    ██   ██  █ █
█   █ █   █ █ █  █ █   █  █ █    ▀█▀
█ █ █ ██  ███ █  █ █   █  █ █ ██  █
██ ██ █   █ █ █  █ █   █  █ █  █  █
█   █ ███ ███  ██  ███  ██   ██   █
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

__version__ = "2025.12.1"

RAINBOW_COLORS = [
    "#ff595e",
    "#ff924c",
    "#ffca3a",
    "#c5ca30",
    "#8ac926",
    "#2ec4b6",
    "#00c2ff",
    "#1982c4",
    "#4267ac",
    "#6a4c93",
    "#8b4ea2",
    "#a26bb3",
    "#ff9ff3",
    "#ff7ab8",
    "#ff6b6b",
] * 4


def make_gradient_text(text: str, colors: list[str], offset: int = 0) -> Text:
    """Create rainbow gradient text."""
    result = Text()
    lines = text.strip().split("\n")
    for line in lines:
        for i, char in enumerate(line):
            color = colors[(i + offset) % len(colors)]
            result.append(char, style=color)
        result.append("\n")
    return result


def animate_logo_until_keypress(console: Console, fps: int = 14) -> int:
    """Animate the logo until a keypress, returning the last color offset."""
    offset = 0
    prompt = Text("Press any key to reveal the card", style="dim")
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setcbreak(fd)
        with Live(console=console, refresh_per_second=fps) as live:
            while True:
                if select.select([sys.stdin], [], [], 0)[0]:
                    sys.stdin.read(1)
                    break
                header = make_gradient_text(ASCII_ART, RAINBOW_COLORS, offset=offset)
                panel = Panel(
                    Align.center(Text.assemble("\n\n", header, "\n\n", prompt, "\n\n")),
                    border_style="bright_blue",
                    title="[bold]webology[/bold]",
                    subtitle="vibe mode",
                )
                live.update(panel)
                time.sleep(1 / fps)
                offset += 1
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return offset


def typing_effect(
    console: Console,
    text: Text,
    panel_title: str,
    delay: float = 0.01,
    cursor: str = "▌",
):
    """Display text with a typing animation effect."""
    displayed = Text()
    plain = text.plain

    # Build a map of character index to style
    style_map = {}
    for span in text._spans:
        for i in range(span.start, span.end):
            style_map[i] = span.style

    with Live(
        Panel(displayed, title=panel_title, border_style="bright_blue"),
        console=console,
        refresh_per_second=60,
    ) as live:
        for i, char in enumerate(plain):
            style = style_map.get(i)
            displayed.append(char, style=style)
            with_cursor = Text.assemble(displayed, (cursor, "bold bright_white"))
            live.update(Panel(with_cursor, title=panel_title, border_style="bright_blue"))
            if char not in " \n":
                time.sleep(delay)
        live.update(Panel(displayed, title=panel_title, border_style="bright_blue"))


def main():
    console = Console()

    # Spinner reveal
    with console.status("[bold cyan]Loading card...", spinner="dots"):
        time.sleep(0.8)

    # Create the card content
    content = Text()
    animate_logo_until_keypress(console)

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
