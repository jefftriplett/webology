import nox

nox.options.default_venv_backend = "uv"


@nox.session(python=["3.9", "3.10", "3.11", "3.12"])
def tests(session: nox.Session) -> None:
    session.install(".", "pytest")
    session.run("pytest")


@nox.session(python="3.12")
def black(session: nox.Session) -> None:
    session.install("black")
    session.run("black", "--check", ".")


@nox.session(python="3.12")
def lint(session: nox.Session) -> None:
    session.install("flake8")
    session.run("flake8")
