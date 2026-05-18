# Contributing to Revenue Holdings

Thank you for your interest in contributing!

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/revenueholdings.git`
3. Create a virtual environment: `python -m venv venv`
4. Install dev dependencies: `pip install -e ".[dev]"`

## Making Changes

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run linting: `ruff check .`
4. Run tests: `python -m pytest tests/ -x`
5. Commit with a descriptive message
6. Push and open a Pull Request

## Code Style

- We use [ruff](https://docs.astral.sh/ruff/) for linting
- Line length: 120 characters
- Python 3.10+ compatible

## Reporting Issues

Please open a GitHub issue with:

- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
