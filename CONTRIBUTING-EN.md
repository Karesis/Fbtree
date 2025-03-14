# FiberTree Contributing Guide

Thank you for your interest in the FiberTree project! We welcome all forms of contributions, whether code contributions, documentation improvements, issue reports, or feature suggestions. This guide will help you understand how to effectively participate in the project.

## Code of Conduct

All contributors participating in this project should respect each other, maintain friendly and constructive communication. We aim to create an inclusive and supportive environment where everyone can freely share ideas and contribute.

## How to Contribute

### Reporting Issues

If you encounter problems while using FiberTree, or have suggestions for improvements, please report them through GitHub Issues. When creating an issue, please:

1. Use a clear, specific title
2. Provide a detailed problem description
3. Include reproduction steps (if applicable)
4. Describe expected behavior and actual behavior
5. Provide environment information (operating system, Python version, etc.)
6. If possible, include relevant code snippets or error logs

### Submitting Pull Requests

If you want to contribute code or documentation, you can submit a Pull Request through the following steps:

1. Fork this repository
2. Create your feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to your branch: `git push origin feature/your-feature-name`
5. Submit a Pull Request to our `main` branch

### Coding Standards

To maintain consistency in the codebase, please follow these coding standards:

- Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) Python style guide
- Use 4 spaces for indentation (not tabs)
- All new code must include appropriate type hints
- Every public function, class, and method must have a docstring
- Ensure your code passes all existing tests
- Write tests for new features you add

### Documentation Contributions

Documentation improvements are a very important form of contribution. You can:

- Improve existing documentation
- Add more examples and tutorials
- Correct errors or outdated information in the documentation
- Improve the structure and readability of the documentation

## Development Environment Setup

Here are the steps to set up a local development environment:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fbtree.git
cd fbtree
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Install pre-commit hooks:
```bash
pre-commit install
```

## Testing

Before submitting a Pull Request, please ensure your code passes all tests:

```bash
pytest
```

For new features you add, please write corresponding tests. We use `pytest` as our testing framework.

## Version Control

We use [Semantic Versioning](https://semver.org/). The version number format is: `major.minor.patch`.

- Major version: Incompatible API changes
- Minor version: Backward-compatible functionality additions
- Patch version: Backward-compatible bug fixes

## Project Structure

Here is the main directory structure of the project:

```
fbtree/
├── core/           # Core functionality modules
├── storage/        # Storage backend implementations
├── analysis/       # Analysis functionality
├── utils/          # Utilities
├── visualization/  # Visualization functionality
tests/              # Test cases
examples/           # Usage examples
docs/               # Documentation
```

## Release Process

Project maintainers will release new versions periodically. The release process is as follows:

1. Update the version number in `setup.py`
2. Update `CHANGELOG.md`
3. Create a new version tag
4. Build and upload to PyPI

## Contact Us

If you have any questions or need help, you can contact us through:

- Submitting an Issue on GitHub
- Sending an email to [project maintainer email]

Thank you again for your contribution to the FiberTree project! 