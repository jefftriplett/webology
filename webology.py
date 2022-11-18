import typer

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel


__doc__ = """### Jeff Triplett / webology

Work: Engineer and Partner at [REVSYS](https://www.revsys.com)

* Website: [jefftriplett.com](https://jefftriplett.com)
* Links: [webology.dev](https://webology.dev)
* GitHub: [@jefftriplett](https://github.com/jefftriplett)
* Mastodon: [@webology@mastodon.social](https://mastodon.social/@webology)
* Twitter: [@webology](https://twitter.com/webology)

**Projects**

* [django-news.com](https://django-news.com)
* [djangopackages.org](https://djangopackages.org)
* [awesomedjango.org](https://awesomedjango.org)
* [djangocon.us](https://djangocon.us)

Card: pipx run webology

"""


def main():
    console = Console()
    md = Markdown(__doc__.strip())
    console.print(Panel.fit(md))


if __name__ == "__main__":
    typer.run(main)
