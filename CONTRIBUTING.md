# Contributing to Survey Automation

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Use the bug report template
3. Include:
   - OS and Python version
   - Steps to reproduce
   - Expected vs actual behavior
   - Logs and screenshots

### Suggesting Features

1. Check if the feature has been suggested
2. Use the feature request template
3. Explain:
   - Use case
   - Expected behavior
   - Potential implementation

### Pull Requests

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Update documentation
6. Run linters and tests
7. Submit PR with clear description

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/survey-automation.git
cd survey-automation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Run linters
black src/
flake8 src/
pylint src/
```

### Code Style

- Follow PEP 8
- Use Black for formatting
- Add docstrings to functions
- Keep functions small and focused
- Write meaningful commit messages

### Testing

- Write tests for new features
- Maintain test coverage >80%
- Test edge cases
- Use pytest fixtures

### Documentation

- Update README for new features
- Add docstrings to code
- Update relevant guides
- Include examples

## Questions?

Open an issue or join our Discord server.

Thank you for contributing! 🎉
