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
