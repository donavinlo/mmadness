import nox

# Default sessions shown when running `nox` without args
nox.options.sessions = ("tests", "tests-local", "ruff", "pylint")


@nox.session(python=["3.10", "3.11", "3.12"])
def tests(session):
    """Run tests in isolated venvs (used by CI).

    Usage:
      nox -s tests           # run all tests (default test discovery)
      nox -s tests -- tests/test_specific.py  # pass specific pytest args/files
    """
    session.install("-r", "requirements-dev.txt")
    session.install(".")
    pytest_args = session.posargs or ["-q", "tests"]
    session.run("pytest", *pytest_args)


@nox.session
def tests_local(session):
    """Run tests in the user's local Python environment (no venv created).

    Usage:
      nox -s tests-local        # runs pytest using the local interpreter
      nox -s tests-local -- path/to/file.py  # test specific files
    """
    pytest_args = session.posargs or ["-q", "tests"]
    # external=True runs the command in the current environment
    session.run("pytest", *pytest_args, external=True)


@nox.session
def ruff(session):
    """Run ruff linting. Supports two special flags in `posargs`:

    - `format` : run `ruff format` to auto-format code
    - `fix`    : run `ruff check --fix` to apply available fixes

    Any other positional args are forwarded to ruff as path/args.
    Examples:
      nox -s ruff         # run ruff check on project
      nox -s ruff -- format  # format code
      nox -s ruff -- fix     # apply lint fixes
    """
    session.install("ruff")
    args = [a for a in session.posargs if a not in ("format", "fix")]
    paths = args or ["."]
    if "format" in session.posargs:
        session.run("ruff", "format", *paths)
    elif "fix" in session.posargs:
        session.run("ruff", "check", "--fix", *paths)
    else:
        session.run("ruff", "check", *paths)


@nox.session
def pylint(session):
    """Run pylint. Pass paths/files as posargs; defaults to `src` and `tests`.

    Examples:
      nox -s pylint
      nox -s pylint -- src/some_module.py
    """
    session.install("pylint")
    targets = session.posargs or ["src", "tests"]
    session.run("pylint", *targets)
