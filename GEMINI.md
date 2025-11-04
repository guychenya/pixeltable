# Pixeltable Project Overview

This document provides a comprehensive overview of the Pixeltable project, its structure, and development workflows. It is intended to be used as a guide for developers and contributors.

## Project Overview

Pixeltable is an open-source Python library that provides declarative data infrastructure for building multimodal AI applications. It simplifies the process of storing, transforming, indexing, retrieving, and orchestrating multimodal data like images, videos, and documents.

### Key Features:

*   **Declarative API:** Define entire data processing and AI workflows using computed columns on tables.
*   **Multimodal Data Handling:** Natively handles various data types including images, videos, audio, and documents.
*   **Incremental Computation:** Automatically recomputes only what's necessary when data or code changes.
*   **AI Integrations:** Built-in support for popular AI/ML libraries and platforms like OpenAI, Hugging Face, and more.
*   **Vector Search:** In-built vector search capabilities for similarity-based queries.
*   **Data Versioning:** Automatically tracks data and schema changes, allowing for "time travel" to previous versions.

### Core Technologies:

*   **Backend:** Python
*   **Database:** PostgreSQL is used for storing structured data.
*   **Dependencies:** The project relies on a wide range of libraries including `numpy`, `pandas`, `sqlalchemy`, `pillow`, `pyarrow`, `torch`, and `transformers`.

## Development Workflow

The project uses a standard set of tools for development, testing, and maintenance. The primary commands are managed through a `Makefile`.

### Initial Setup

1.  **Prerequisites:**
    *   `git`
    *   `make`
    *   `conda`

2.  **Environment Setup:**
    *   Create and activate a conda environment:
        ```bash
        conda create --name pxt python=3.10
        conda activate pxt
        ```

3.  **Installation:**
    *   Clone the repository and install the dependencies:
        ```bash
        git clone https://github.com/<your-username>/pixeltable.git
        cd pixeltable
        make install
        ```

### Building and Running

The project is a library, so there isn't a single "run" command. Development typically involves writing and running Python scripts that import and use the `pixeltable` library.

### Testing

The project has a comprehensive test suite.

*   **Run all basic tests:**
    ```bash
    make test
    ```
*   **Run the full test suite (including expensive tests):**
    ```bash
    make fulltest
    ```
*   **Run a minimal set of tests:**
    ```bash
    make slimtest
    ```
*   **Run tests on notebooks:**
    ```bash
    make nbtest
    ```

### Code Quality and Formatting

The project uses `ruff` for linting and formatting, and `mypy` for type checking.

*   **Check for linting and formatting issues:**
    ```bash
    make check
    ```
*   **Automatically format the code:**
    ```bash
    make format
    ```
*   **Run the type checker:**
    ```bash
    make typecheck
    ```

### Documentation

The project's documentation is built using `mkdocs`.

*   **Build the documentation locally:**
    ```bash
    make docs-local
    ```
    Then, to preview the documentation, run `cd docs/target && npx mintlify dev`.

## Contribution Guidelines

Contributions to Pixeltable are welcome. The project follows a standard fork-and-pull request model.

1.  Fork the repository on GitHub.
2.  Clone your fork locally.
3.  Create a new branch for your changes.
4.  Make your changes, ensuring to add or update tests as needed.
5.  Format your code with `make format`.
6.  Run the tests with `make test`.
7.  Push your changes to your fork and open a pull request.
