# mmadness
Project for data engineering for march madness predictive modelling

Quick setup
-----------

Install dev dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Run tests with nox:

```bash
nox -s tests
```

Run ruff linting:

```bash
nox -s ruff
```

Run pylint:

```bash
nox -s pylint
```

