![CI](https://github.com/taleldayekh/talel.io-backend/workflows/CI/badge.svg) ![CD](https://github.com/taleldayekh/talel.io-backend/workflows/CD/badge.svg) [![codecov](https://codecov.io/gh/taleldayekh/talel.io-backend/branch/develop/graph/badge.svg)](https://codecov.io/gh/taleldayekh/talel.io-backend)

# Table of Contents

- [Setup](#setup)
  - [Clone Repository](#clone-repository)
  - [Setup Python](#setup-python)
  - [Install Dependencies](#install-dependencies)
- [Running the API Locally](#running-the-api-locally)
  - [Start Development Database](#start-development-database)
  - [Stop Development Database](#stop-development-database)
  - [Serve API](#serve-api)
- [Codebase](#codebase)
  - [Code Style](#code-style)
- [REST API](#rest-api)

# Setup

## Clone Repository

```shell
git clone git@github.com:taleldayekh/talel.io-backend.git
```

## Setup Python

### pyenv

[pyenv (Python Version Management)](https://github.com/pyenv/pyenv) can be used for easily managing Python versions globally on the system and locally for a project.

Install pyenv with:

```shell
brew install pyenv
```

Set the project specific Python version defined in the [`Pipfile`](https://github.com/taleldayekh/talel.io-backend/blob/develop/Pipfile) by navigating to the project root and running:

```shell
pyenv local <version>
```

### Pipenv

`talel.io-backend` uses [Pipenv](https://github.com/pypa/pipenv) for managing the projects virtual environment and dependencies.

Install Pipenv with:

```shell
brew install pipenv
```

Activate the virtual environment for `talel.io-backend` by navigating to the project root and running:

```shell
pipenv shell
```

## Install Dependencies

> ⚠️ Dependency installation will fail if PostgreSQL is not installed on the system.

Install PostgreSQL:

```shell
brew install postgresql@14
```

Install dependencies and dev dependencies by navigating to the project root and running:

```shell
pipenv install --dev
```

# Running the API Locally

## Start Development Database

The development database runs in a Docker container and requires [Docker Desktop](https://docs.docker.com/desktop/) installed and running.

Install Docker Desktop:

```shell
brew install --cask docker
```

Start development database container:

```shell
make start-dev-dbs
```

This will start a PostgreSQL database configured for development and run the most recent migrations.

## Stop Development Database

Stop development database container:

```shell
make stop-dev-dbs
```

## Serve API

Before serving the API ensure there is a `.env` present in the project root containing the same values as in [`.env.example`](https://github.com/taleldayekh/talel.io-backend/blob/develop/.env.example).

Serve backend API:

```shell
make serve-api
```

This will run the development server on port `5000`.

# Codebase

## Code Style

To maintain consistency across the codebase, coding standards that conforms to the [PEP 8](https://peps.python.org/pep-0008/) style guide are enforced with:

- [YAPF](https://github.com/google/yapf) for formatting the code.
- [isort](https://github.com/PyCQA/isort) for sorting imports.

To help detect coding errors the following static code analysis tools are used:

- [mypy](https://github.com/python/mypy) for providing type hints.
- [Pylint](https://github.com/pylint-dev/pylint) for checking coding errors.

### Formatters

Run formatters:

```shell
make fix
```

### Code Analysis

Run code analysis:

```shell
make type-check
```

```shell
make lint
```

# REST API

Full API reference documentation is available on the [Wiki page](https://github.com/taleldayekh/talel.io-backend/wiki/REST-API).
