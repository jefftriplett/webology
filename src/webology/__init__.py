import random
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
  Bluesky:  @webology.bsky.social
  Mastodon: @webology@mastodon.social
  X:        @webology

Projects
  • django-news.com
  • djangopackages.org
  • awesomedjango.org
  • djangocon.us
  • djangojobboard.com
  • djangotv.com
  • upgradedjango.com
  • djangowebring.com
  • djangotemplatetagsandfilters.com

Card: uvx webology
"""

__version__ = "2026.5.2"

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


def make_gradient_text(
    text: str, colors: list[str], offset: int = 0, sparkle: float = 0.0
) -> Text:
    """Create rainbow gradient text with optional sparkle effect."""
    result = Text()
    lines = text.strip().split("\n")
    for line in lines:
        for i, char in enumerate(line):
            if sparkle > 0 and char != " " and random.random() < sparkle:
                result.append(char, style="bold bright_white")
            else:
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
                header = make_gradient_text(
                    ASCII_ART, RAINBOW_COLORS, offset=offset, sparkle=0.08
                )
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


def dissolve_effect(
    console: Console,
    text: Text,
    panel_title: str,
    batch_size: int = 3,
    delay: float = 0.008,
):
    """Reveal text with a random pixel dissolve like classic Sierra games."""
    plain = text.plain
    length = len(plain)

    style_map = {}
    for span in text._spans:
        for i in range(span.start, span.end):
            style_map[i] = span.style

    revealed = [False] * length
    # Pre-mark spaces and newlines as revealed
    for i, char in enumerate(plain):
        if char in " \n":
            revealed[i] = True

    # Build the random reveal order for non-whitespace characters
    unrevealed = [i for i in range(length) if not revealed[i]]
    random.shuffle(unrevealed)

    with Live(
        Panel(Text(" "), title=panel_title, border_style="bright_blue"),
        console=console,
        refresh_per_second=60,
    ) as live:
        for batch_start in range(0, len(unrevealed), batch_size):
            batch = unrevealed[batch_start : batch_start + batch_size]
            for idx in batch:
                revealed[idx] = True

            displayed = Text()
            for i, char in enumerate(plain):
                if revealed[i]:
                    displayed.append(char, style=style_map.get(i))
                else:
                    displayed.append(" ")

            live.update(
                Panel(displayed, title=panel_title, border_style="bright_blue")
            )
            time.sleep(delay)

        # Final clean render
        final = Text()
        for i, char in enumerate(plain):
            final.append(char, style=style_map.get(i))
        live.update(Panel(final, title=panel_title, border_style="bright_blue"))


def export_svg(path: str = "webology.svg"):
    """Export the logo screen as an SVG file."""
    console = Console(record=True, width=80)
    header = make_gradient_text(ASCII_ART, RAINBOW_COLORS, offset=0)
    prompt = Text("Press any key to reveal the card", style="dim")
    panel = Panel(
        Align.center(Text.assemble("\n\n", header, "\n\n", prompt, "\n\n")),
        border_style="bright_blue",
        title="[bold]webology[/bold]",
        subtitle="vibe mode",
    )
    console.print(panel)
    svg = console.export_svg(title="webology")
    with open(path, "w") as f:
        f.write(svg)
    Console().print(f"[green]Exported SVG to {path}[/green]")


def version_callback(value: bool):
    if value:
        typer.echo(f"webology {__version__}")
        raise typer.Exit()


LINK_MAP = {
    "https://www.revsys.com": "https://www.revsys.com",
    "jefftriplett.com": "https://jefftriplett.com",
    "webology.dev": "https://webology.dev",
    "@jefftriplett": "https://github.com/jefftriplett",
    "@webology.bsky.social": "https://bsky.app/profile/webology.bsky.social",
    "@webology@mastodon.social": "https://mastodon.social/@webology",
    "@webology": "https://x.com/webology",
    "django-news.com": "https://django-news.com",
    "djangopackages.org": "https://djangopackages.org",
    "awesomedjango.org": "https://awesomedjango.org",
    "djangocon.us": "https://djangocon.us",
    "djangojobboard.com": "https://djangojobboard.com",
    "djangotv.com": "https://djangotv.com",
    "upgradedjango.com": "https://upgradedjango.com",
    "djangowebring.com": "https://djangowebring.com",
    "djangotemplatetagsandfilters.com": "https://djangotemplatetagsandfilters.com",
}


def _linkify(text: str, base_style: str = "") -> Text:
    """Return a Text object with clickable links for known tokens."""
    result = Text()
    remaining = text
    sorted_tokens = sorted(LINK_MAP.keys(), key=len, reverse=True)
    while remaining:
        match = None
        earliest_pos = len(remaining)
        for token in sorted_tokens:
            pos = remaining.find(token)
            if pos != -1 and pos < earliest_pos:
                earliest_pos = pos
                match = (pos, token, LINK_MAP[token])
        if match is None:
            result.append(remaining, style=base_style)
            break
        pos, token, url = match
        if pos > 0:
            result.append(remaining[:pos], style=base_style)
        result.append(token, style=f"{base_style} link {url}".strip())
        remaining = remaining[pos + len(token) :]
    return result


def build_card_content() -> Text:
    """Build styled card content as a Rich Text object."""
    content = Text()
    lines = CARD_CONTENT.strip().split("\n")
    for line in lines:
        if line.startswith("Work:"):
            content.append_text(_linkify(line, "italic"))
            content.append("\n")
        elif line.startswith("Projects"):
            content.append("\n" + line + "\n", style="bold bright_magenta")
        elif line.strip().startswith("•"):
            content.append_text(_linkify(line, "bright_green"))
            content.append("\n")
        elif line.startswith("Card:"):
            content.append("\n" + line + "\n", style="dim italic")
        elif ":" in line.strip() and line.strip()[0].isalpha():
            parts = line.split(":", 1)
            content.append(parts[0] + ":", style="bold cyan")
            content.append_text(_linkify(parts[1], "white"))
            content.append("\n")
        else:
            content.append(line + "\n")
    return content


def show_static_card(console: Console):
    """Show the card without animation (for piped output or --no-animate)."""
    header = make_gradient_text(ASCII_ART, RAINBOW_COLORS, offset=0)
    content = build_card_content()
    full = Text.assemble(header, "\n", content)
    console.print(
        Panel(full, title="[bold]Jeff Triplett[/bold]", border_style="bright_blue")
    )


def main(
    svg: bool = typer.Option(False, "--svg", help="Export logo as SVG"),
    card: bool = typer.Option(False, "--card", help="Show card without logo animation"),
    no_animate: bool = typer.Option(
        False, "--no-animate", help="Show card without any animation"
    ),
    version: bool = typer.Option(
        False,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
):
    if svg:
        export_svg()
        return

    console = Console()

    if no_animate or not sys.stdout.isatty():
        show_static_card(console)
        return

    if not card:
        animate_logo_until_keypress(console)

    content = build_card_content()
    dissolve_effect(console, content, "[bold]Jeff Triplett[/bold]")


def cli():
    typer.run(main)


if __name__ == "__main__":
    cli()
