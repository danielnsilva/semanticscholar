# Contributing Guidelines

Thank you for your interest in contributing to the project! This document will help you get started. There are many ways to contribute:

- Participate in discussions
- Report issues or suggest improvements
- Contribute with code to fix bugs or add features
- Improve the documentation

## Reporting issues

If you find a bug or have a suggestion for improvement, please open an issue. Before doing so, make sure to search for existing ones to avoid duplicates.

When opening a new issue, provide as much information as possible. The templates provided will guide you on what to include. In general, the more details you provide, the easier it will be to understand and address the problem.

[Short, self-contained, correct examples](https://sscce.org/) are always appreciated. If you can provide a code snippet that reproduces the issue, it will be very helpful.

Debug information is also important. See the [troubleshooting section in the docs](https://semanticscholar.readthedocs.io/en/stable/usage.html#troubleshooting) to learn how to gather it. Be sure to exclude any sensitive data.

## Contributing with code

All code contributions must be made through Pull Requests.

When contributing, please:

- Follow the PEP8 style guide: Ensure your code is clean and readable by following the [PEP8 style guide](https://www.python.org/dev/peps/pep-0008/).
- Include tests: Write the necessary tests to verify your code works. Ensure all tests pass before submitting a PR.
- Avoid breaking changes: If necessary, mention them clearly in the PR description.
- Update documentation: Update or add documentation for new or changed features.
- Follow commit message conventions: Although not mandatory, we encourage following the [Conventional Commits](https://www.conventionalcommits.org/) specification to maintain a clean and organized commit history.

### Running and writing tests

First, install the dependencies:

```console
pip install -r test-requirements.txt
```

Then, run the tests:

1. Run all tests:

    ```console
    python -m unittest
    ```

2. Run all tests in a specific class:

    ```console
    python -m unittest tests.test_semanticscholar.TestClassName
    ```

3. Run a specific test method:

    ```console
    python -m unittest tests.test_semanticscholar.TestClassName.testMethod
    ```

### Recording API Calls

This project uses a [modified version](https://github.com/danielnsilva/vcrpy) of [VCR.py](https://github.com/kevin1024/vcrpy), a library designed to record HTTP interactions and replay them during tests, eliminating the need to make actual HTTP requests repeatedly.

When adding new tests, the first run will record the interactions and save them as a new file in the `tests/data` directory.

The modification ensures that **unused recorded interactions are removed** during the test run. This helps to maintain clean and relevant recorded data, avoiding the accumulation of outdated or unnecessary interactions over time.

### Code coverage

When adding new code, make sure to write tests that cover it. The goal is to maintain high code coverage.

To check the code coverage, run:

```console
python -m coverage run --source=semanticscholar/ -m unittest discover
```

To generate a report, run:

```console
python -m coverage report
```

If you want to see the coverage in HTML format, run:

```console
python -m coverage html
```

## Contributing to documentation

The documentation is built using [Sphinx](https://www.sphinx-doc.org/en/master/) and hosted on [Read the Docs](https://readthedocs.org/).

To get started, install the necessary dependencies:

```console
pip install -r docs-requirements.txt
```

After add new content, you could build the documentation locally:

```console
cd docs && make html
```

Then, open the `docs/build/html/index.html` file in your browser to see the changes.

Please do not include auto-generated files, such as those created by `docs/source/conf.py`, in your PRs.

To contribute to the documentation, it's important to be familiar with **reStructuredText** and **Sphinx**. For more details on how to work with them, refer to the [official Sphinx documentation](https://www.sphinx-doc.org/en/master/usage/index.html).
