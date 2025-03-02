# Contributing to Flight Data API

Thank you for considering contributing to the Flight Data API! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports:

1. Check the issue tracker to see if the problem has already been reported
2. If you're unable to find an open issue addressing the problem, open a new one

When reporting bugs, include as much information as possible:
- A clear and descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Screenshots if applicable
- Environment details (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

1. Use a clear and descriptive title
2. Provide a detailed description of the suggested enhancement
3. Explain why this enhancement would be useful

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure your changes don't break existing functionality
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/flight-data-api.git
cd flight-data-api
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a test database or use the provided one

## Testing

Run tests with:
```bash
pytest
```

## Style Guidelines

This project follows:
- PEP 8 for Python code style
- Google style for docstrings

We use the following tools for code quality:
- flake8 for linting
- black for code formatting

Before submitting a pull request, please run:
```bash
flake8 .
black .
```

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.