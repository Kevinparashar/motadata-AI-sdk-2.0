# Development Extensions & Tools

This document lists recommended extensions, tools, and configurations to enhance the development experience for the Metadata Python SDK.

## Table of Contents

- [VS Code / Cursor Extensions](#vs-code--cursor-extensions)
- [Python Development Tools](#python-development-tools)
- [Pre-commit Hooks](#pre-commit-hooks)
- [Documentation Tools](#documentation-tools)
- [Development Workflow](#development-workflow)
- [VS Code Settings](#vs-code-settings)

---

## VS Code / Cursor Extensions

### Essential Extensions

1. **Python** (Microsoft)
   - Python language support, IntelliSense, debugging, linting
   - Extension ID: `ms-python.python`

2. **Pylance** (Microsoft)
   - Fast, feature-rich language server for Python
   - Extension ID: `ms-python.vscode-pylance`

3. **Python Docstring Generator** (Nils Werner)
   - Auto-generate docstrings following Google, NumPy, or Sphinx style
   - Extension ID: `nils-werner.python-docstring-generator`

4. **autoDocstring** (Nils Werner)
   - Generate Python docstrings automatically
   - Extension ID: `njpwerner.autodocstring`

### Code Quality Extensions

5. **Black Formatter** (Microsoft)
   - Official Black formatter extension
   - Extension ID: `ms-python.black-formatter`

6. **isort** (Microsoft)
   - Import sorting using isort
   - Extension ID: `ms-python.isort`

7. **Flake8** (Microsoft)
   - Linting using flake8
   - Extension ID: `ms-python.flake8`

8. **mypy Type Checker** (Microsoft)
   - Static type checking with mypy
   - Extension ID: `ms-python.mypy-type-checker`

9. **Ruff** (Astral Software)
   - Fast Python linter and formatter (alternative to flake8 + black)
   - Extension ID: `charliermarsh.ruff`

### Testing Extensions

10. **Python Test Explorer** (Little Fox Team)
    - Test discovery and execution for pytest
    - Extension ID: `littlefoxteam.vscode-python-test-adapter`

11. **Coverage Gutters** (ryanluker)
    - Display test coverage in the editor
    - Extension ID: `ryanluker.vscode-coverage-gutters`

### Git & Version Control

12. **GitLens** (GitKraken)
    - Enhanced Git capabilities, blame annotations, file history
    - Extension ID: `eamodio.gitlens`

13. **Git History** (Don Jayamanne)
    - View git log, file history, compare branches
    - Extension ID: `donjayamanne.githistory`

### Documentation & Markdown

14. **Markdown All in One** (Yu Zhang)
    - Markdown editing, preview, table of contents
    - Extension ID: `yzhang.markdown-all-in-one`

15. **Markdown Preview Enhanced** (Yiyi Wang)
    - Enhanced markdown preview with diagrams
    - Extension ID: `shd101wyy.markdown-preview-enhanced`

### Productivity Extensions

16. **Error Lens** (Alexander)
    - Highlight errors and warnings inline
    - Extension ID: `usernamehw.errorlens`

17. **Better Comments** (Aaron Bond)
    - Improve code comments with annotations
    - Extension ID: `aaron-bond.better-comments`

18. **Todo Tree** (Gruntfuggly)
    - Show TODO, FIXME, etc. comments in a tree view
    - Extension ID: `gruntfuggly.todo-tree`

19. **indent-rainbow** (oderwat)
    - Colorize indentation for better readability
    - Extension ID: `oderwat.indent-rainbow`

20. **Bracket Pair Colorizer 2** (CoenraadS)
    - Colorize matching brackets
    - Extension ID: `coenraads.bracket-pair-colorizer-2`

### AI & Code Assistance

21. **GitHub Copilot** (GitHub)
    - AI pair programmer (if you have access)
    - Extension ID: `github.copilot`

22. **Codeium** (Codeium)
    - Free AI code completion alternative
    - Extension ID: `codeium.codeium`

---

## Python Development Tools

### Additional Development Dependencies

Add these to `pyproject.toml` under `[project.optional-dependencies]`:

```toml
dev = [
    # ... existing tools ...
    
    # Additional code quality
    "ruff>=0.1.0",              # Fast linter (alternative to flake8)
    "pydocstyle>=6.3.0",       # Docstring style checker
    "pydantic-settings>=2.0.0", # Settings management
    
    # Development utilities
    "ipython>=8.0.0",          # Enhanced Python REPL
    "ipdb>=0.13.0",            # IPython debugger
    "rich>=13.0.0",            # Rich terminal formatting
    "typer>=0.9.0",            # CLI framework
    
    # Documentation
    "mkdocs>=1.5.0",           # Documentation generator
    "mkdocs-material>=9.0.0",  # Material theme for mkdocs
    "mkdocstrings[python]>=0.22.0", # Auto-generate API docs
    
    # Performance profiling
    "py-spy>=0.3.14",          # Sampling profiler
    "memory-profiler>=0.61.0", # Memory profiler
    
    # Type checking enhancements
    "types-requests>=2.31.0",   # Type stubs for requests
    "types-python-dateutil>=2.8.0", # Type stubs
]
```

### Install Additional Tools

```bash
# Install with UV
uv add --dev ruff pydocstyle ipython rich typer mkdocs mkdocs-material

# Or add to pyproject.toml and sync
uv sync --all-extras
```

---

## Pre-commit Hooks

### Setup Pre-commit Configuration

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-json
      - id: check-toml
      - id: check-merge-conflict
      - id: debug-statements
      - id: mixed-line-ending

  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.8

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=100, --extend-ignore=E203]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests, types-python-dateutil]
        args: [--ignore-missing-imports]

  - repo: https://github.com/pycqa/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-r, src/, -f, json]

  - repo: https://github.com/PyCQA/pydocstyle
    rev: 6.3.0
    hooks:
      - id: pydocstyle
        args: [--convention=google]

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
```

### Install Pre-commit Hooks

```bash
# Install pre-commit
uv add --dev pre-commit

# Install git hooks
uv run pre-commit install

# Run on all files (first time)
uv run pre-commit run --all-files
```

---

## Documentation Tools

### MkDocs Configuration

Create `mkdocs.yml`:

```yaml
site_name: Metadata Python SDK
site_description: Python SDK for Metadata AI platform
site_author: Metadata AI Team

theme:
  name: material
  palette:
    - scheme: default
      primary: blue
      accent: blue
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    - scheme: slate
      primary: blue
      accent: blue
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.tabs
    - navigation.sections
    - toc.integrate

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          paths: [src]

nav:
  - Home: index.md
  - Getting Started: getting-started.md
  - Core Components: CORE_COMPONENTS.md
  - Architecture: ARCHITECTURE.md
  - API Reference:
    - Core: api/core.md
    - Agents: api/agents.md
    - AI Gateway: api/ai_gateway.md
    - Database: api/database.md
    - API: api/api.md
    - Codecs: api/codecs.md
    - Config: api/config.md
  - Contributing: CONTRIBUTING.md
```

### Generate Documentation

```bash
# Build documentation
uv run mkdocs build

# Serve documentation locally
uv run mkdocs serve

# Deploy to GitHub Pages
uv run mkdocs gh-deploy
```

---

## Development Workflow

### Useful UV Commands

```bash
# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev package-name

# Update all dependencies
uv sync --upgrade

# Run a command in the virtual environment
uv run python script.py
uv run pytest
uv run black .
uv run mypy src/

# Show dependency tree
uv tree

# Export requirements
uv pip compile pyproject.toml -o requirements.txt
```

### Development Scripts

Add to `pyproject.toml`:

```toml
[project.scripts]
sdk-format = "black:main"
sdk-lint = "flake8:main"
sdk-type-check = "mypy:main"
sdk-test = "pytest:main"
```

---

## VS Code Settings

### Create `.vscode/settings.json`

```json
{
  // Python settings
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.analysis.typeCheckingMode": "basic",
  "python.analysis.autoImportCompletions": true,
  "python.analysis.diagnosticMode": "workspace",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,
  "python.linting.pylintEnabled": false,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "100"],
  "python.sortImports.args": ["--profile", "black"],
  
  // Editor settings
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": "explicit"
  },
  "editor.rulers": [100],
  "editor.tabSize": 4,
  "editor.insertSpaces": true,
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/.pytest_cache": true,
    "**/.mypy_cache": true,
    "**/.venv": true
  },
  
  // File associations
  "files.associations": {
    "*.md": "markdown"
  },
  
  // Test settings
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": [
    "src/tests"
  ],
  
  // Coverage settings
  "coverage-gutters.coverageFileNames": [
    ".coverage",
    "coverage.xml"
  ],
  
  // Markdown settings
  "markdown.preview.breaks": true,
  "markdown.preview.fontSize": 14
}
```

### Create `.vscode/extensions.json`

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.black-formatter",
    "ms-python.isort",
    "ms-python.flake8",
    "ms-python.mypy-type-checker",
    "charliermarsh.ruff",
    "njpwerner.autodocstring",
    "littlefoxteam.vscode-python-test-adapter",
    "ryanluker.vscode-coverage-gutters",
    "eamodio.gitlens",
    "yzhang.markdown-all-in-one",
    "usernamehw.errorlens",
    "gruntfuggly.todo-tree",
    "oderwat.indent-rainbow"
  ]
}
```

### Create `.vscode/launch.json` (for debugging)

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": true,
      "env": {
        "PYTHONPATH": "${workspaceFolder}/src"
      }
    },
    {
      "name": "Python: Pytest",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": [
        "src/tests",
        "-v"
      ],
      "console": "integratedTerminal",
      "justMyCode": false
    }
  ]
}
```

---

## Quick Setup Commands

```bash
# 1. Install all recommended extensions (VS Code)
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-python.black-formatter
code --install-extension ms-python.isort
code --install-extension ms-python.flake8
code --install-extension ms-python.mypy-type-checker
code --install-extension charliermarsh.ruff
code --install-extension njpwerner.autodocstring
code --install-extension littlefoxteam.vscode-python-test-adapter
code --install-extension ryanluker.vscode-coverage-gutters
code --install-extension eamodio.gitlens
code --install-extension yzhang.markdown-all-in-one
code --install-extension usernamehw.errorlens
code --install-extension gruntfuggly.todo-tree

# 2. Install additional Python tools
uv add --dev ruff pydocstyle ipython rich typer mkdocs mkdocs-material

# 3. Setup pre-commit hooks
uv run pre-commit install

# 4. Run pre-commit on all files
uv run pre-commit run --all-files
```

---

## Benefits

### Code Quality
- ✅ Automatic formatting on save
- ✅ Real-time linting and type checking
- ✅ Consistent code style across the project
- ✅ Pre-commit hooks prevent bad commits

### Developer Experience
- ✅ Better IntelliSense and autocomplete
- ✅ Inline error highlighting
- ✅ Test discovery and execution
- ✅ Coverage visualization
- ✅ Git integration and history

### Documentation
- ✅ Auto-generated API documentation
- ✅ Beautiful documentation site
- ✅ Docstring generation
- ✅ Markdown preview with diagrams

### Productivity
- ✅ AI code completion
- ✅ TODO tracking
- ✅ Better comments and annotations
- ✅ Enhanced debugging capabilities

---

## Next Steps

1. **Install VS Code Extensions**: Use the recommendations in `.vscode/extensions.json`
2. **Setup Pre-commit**: Create `.pre-commit-config.yaml` and install hooks
3. **Configure VS Code**: Use the settings from `.vscode/settings.json`
4. **Add Development Tools**: Install additional Python tools with UV
5. **Setup Documentation**: Configure MkDocs for API documentation

---

**Note**: Some extensions may require additional configuration or licenses. Check individual extension documentation for details.

