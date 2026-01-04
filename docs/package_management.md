# Package Management & Project Packaging (uv + pyproject.toml)

This project is managed using **uv** and a **`pyproject.toml`-based** build.  
The repository is structured as an installable Python package so imports are consistent and reliable across modules, tests, and services.

The goal is to support:

- reproducible dependency management
- clean imports (no `sys.path` hacks)
- editable installs for local development (`-e .`)
- CI-friendly installs
- a layout that scales as modules grow

---

## 1. Why package the repo?

Packaging the project (instead of treating it like a loose folder of scripts) gives:

- **stable imports** (`from decisioning.engine...` works everywhere)
- **one source of truth** for dependencies (`pyproject.toml`)
- **easy local dev** via editable install (`pip install -e .`)
- cleaner tests (pytest imports work without path hacks)
- simpler deployment/containers (install the package in the image)

---

## 2. Tooling Choice

### uv
`uv` is used for:
- fast dependency installation
- locked environments
- running commands inside the managed environment

### pyproject.toml
`pyproject.toml` is used for:
- project metadata (name/version)
- dependency declarations
- build backend configuration
- tool configs (ruff, pytest, etc.)

---

## 3. Recommended Repository Layout (src layout)

Use a `src/` layout so Python imports always resolve through the installed package, not the working directory.

```txt
decisioning-system/
  pyproject.toml
  README.md
  docs/
  src/
    decisioning/
      __init__.py
      engine/
        __init__.py
        modules/
          __init__.py
          eligibility.py
          bureau.py
          servicing.py
          verification.py
          decisioning.py
        orchestrator.py
        contracts.py
        context.py
      ml/
        __init__.py
        train.py
        score.py
        evaluate.py
      service/
        __init__.py
        api.py
        storage.py
      chat/
        __init__.py
        explain.py
        prompts/
  tests/
    test_orchestrator.py
    test_rules.py
```

# Package Management & Packaging (uv + pyproject.toml)

This document describes how the project manages dependencies and is packaged as an installable Python package using **uv** and **pyproject.toml**, enabling clean imports and an editable install workflow (`pip install -e .`).

---

## Why `src/` Layout Is Preferred

The `src/` layout is recommended because it:

- prevents accidental imports from the repository root  
- ensures tests/imports behave the same locally and in CI  
- matches common production repo patterns  

In a non-`src/` layout, Python may import modules from the working directory (repo root) in ways that hide packaging issues until CI or Docker.

---

## `pyproject.toml` (Starter Template)

Adjust `name`, `description`, and dependency versions as needed.

```toml
[project]
name = "decisioning-system"
version = "0.1.0"
description = "Modular credit decisioning platform with explainable outcomes"
readme = "README.md"
requires-python = ">=3.11"
authors = [{ name = "Raghav", email = "you@example.com" }]

dependencies = [
  "polars>=1.0.0",
  "fastapi>=0.110",
  "uvicorn>=0.27",
  "pydantic>=2.6",
  "duckdb>=1.0.0",
  "pyarrow>=15.0.0"
]

[project.optional-dependencies]
dev = [
  "pytest>=8.0",
  "ruff>=0.6",
  "mypy>=1.10",
  "pre-commit>=3.7",
  "types-requests"
]

[build-system]
requires = ["hatchling>=1.25"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/decisioning"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q"

[tool.ruff]
line-length = 100
target-version = "py311"
src = ["src"]

[tool.mypy]
python_version = "3.11"
mypy_path = ["src"]
strict = false
```

## Notes

- Using **hatchling** as the build backend is simple and modern.
- `packages = ["src/decisioning"]` ensures the `decisioning` package is included in the build.

---

## Create the Package Skeleton

### Minimum required files

- `src/decisioning/__init__.py`
- `src/decisioning/engine/__init__.py`
- `src/decisioning/engine/modules/__init__.py`

### Example `src/decisioning/__init__.py`

```python
__all__ = ["engine", "ml", "service", "chat"]
__version__ = "0.1.0"
```






## Using uv for Installs & Running Commands
### Create / sync the environment
```bash
uv sync
```

### Install development dependencies
```bash
uv sync --extra dev
```

### Run tests
```bash
uv run pytest
```

### Run the API
```bash
uv run uvicorn decisioning.service.api:app --reload
```

### Editable Install (-e .) for Easy Imports
Editable installs make imports work consistently from anywhere in the repository.

Example:
```python
from decisioning.engine.orchestrator import Orchestrator
```

### Option A (preferred): editable install via pip
```bash
uv run pip install -e .
```

### Option B: sync dev dependencies, then editable install
```bash
uv sync --extra dev
uv run pip install -e .
```


After this, imports resolve through the installed package rather than relative paths.

### Import Conventions (Keep It Clean)

Always import from the top-level package name.

### Good
```python
from decisioning.engine.context import DecisionContext
from decisioning.engine.modules.bureau import BureauModule
```

### Avoid
```python
from engine.context import DecisionContext
from ..modules.bureau import BureauModule
```


This reduces relative import confusion and makes refactors safer.

### CI / Reproducibility Expectations

Minimum reproducibility expectations for this repository:

pyproject.toml is the single dependency definition

uv manages the environment

tests run using uv run pytest

no global Python dependencies are required

### Common Pitfalls (and How We Avoid Them)

Import errors in tests
Use src/ layout + editable install

Code works locally but fails in containers
Always run via uv run ... and install the package in Docker

Accidental local path imports
src/ layout prevents this

### Definition of Done (Package Management)

This section is considered complete when:

uv sync succeeds on a fresh machine

uv run pytest runs without import hacks

uv run uvicorn decisioning.service.api:app --reload works

importing any module via from decisioning... works anywhere

pip install -e . is documented and functional

### Optional Extensions

If needed, add:

a matching Makefile (e.g. make test, make run-api)

a minimal Dockerfile that installs the package cleanly

a pre-commit configuration for ruff + formatting