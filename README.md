![CI](https://github.com/taleldayekh/talel.io-backend/workflows/CI/badge.svg) ![CD](https://github.com/taleldayekh/talel.io-backend/workflows/CD/badge.svg) [![codecov](https://codecov.io/gh/taleldayekh/talel.io-backend/branch/develop/graph/badge.svg)](https://codecov.io/gh/taleldayekh/talel.io-backend)

# Table of Contents

- [Development](#development)
  - [Setup](#setup)
  - [Code Style](#code-style)
  - [Testing](#testing)
  - [CI/CD](#cicd)
- [Deployment](#deployment)
  - [Infrastructure Diagram](#infrastructure-diagram)
  - [AWS ECR](#aws-ecr-elastic-container-registry)
  - [AWS ECS](#aws-ecs-elastic-container-service)

# Development

## Setup

1. **Clone repository**  

   ```bash
   git clone git@github.com:taleldayekh/talel.io-backend.git
   ```

2. **Set Git Hooks path**  

   This is necessary for using the hooks located in the `.githooks` directory. The path is added locally for the git config of this repository.

   ```bash
   make set-githooks-path
   ```

## Code Style

To maintain consistency across the codebase, coding standards that conforms to the _*PEP 8*_ style guide are enforced with the help of:

- [YAPF](https://github.com/google/yapf) for reformatting the code.  

- [isort](https://github.com/PyCQA/isort) for sorting and separating imports.  
  
  ```bash
  make fix
  ```

To help detect errors and reduce bugs the following static code analysis tools are used:

- [mypy](https://github.com/python/mypy) for checking type errors.  
  
  ```bash
  make type-check
  ```

- [Pylint](https://github.com/PyCQA/pylint) for checking programming errors.  
  
  ```bash
  make lint
  ```

## Testing

Tests are written using the [pytest](https://github.com/pytest-dev/pytest) framework and test coverage reports are generated with [pytest-cov](https://github.com/pytest-dev/pytest-cov) and uploaded to [codecov.io](https://codecov.io/).

**Run tests**

```bash
make test
```

**Run tests and generate coverage XML file**

Test coverage is only uploaded to Codecov in the CI pipeline.

```bash
make test-coverage
```

## CI/CD

[GitHub Actions](https://docs.github.com/en/free-pro-team@latest/actions) is used for _*Continuous Integration*_ and _*Continuous Deployment*_. The CI pipeline runs when a pull request is created to the `develop` branch and the CD pipeline runs when code is merged to the `main` branch.

### CI

Runs all test suites and lint tools.

### CD

Runs all test suites before building the Docker image artifact of the application backend which is then pushed to and deployed on AWS.

# Deployment

## Infrastructure Diagram

```
╭── GitHub ──╮         ╭─── AWS ECR ───╮         ╭─── AWS ECS ───╮
│            │ ──────► │ Server Images │ ──────► │ ╭───────────╮ │         ╭──────────────╮
│     CD     │         ╰───────────────╯         │ │           │ │         │              │
│  Pipeline  │                                   │ │    EC2    │ │ ──────► │ www.talel.io │
│            │         ╭─── AWS ECR ───╮         │ │           │ │         │              │
│            │ ──────► │ Client Images │ ──────► │ ╰───────────╯ │         ╰──────────────╯
╰────────────╯         ╰───────────────╯         ╰───────────────╯
```

## AWS ECR (Elastic Container Registry)

The Docker image artifacts which represents the application backend and frontend are hosted with [Amazon Elastic Container Registry](https://aws.amazon.com/ecr/).

Each image has its separate repository containing all versions of a given image. The lifecycle policy for the repositories is however set to only keep the latest version of an image.

## AWS ECS (Elastic Container Service)

[Amazon Elastic Container Service](https://aws.amazon.com/ecs/) orchestration platform manages and deploys Docker containers based on the images from the ECR.

The _*talelio*_ ECS cluster (grouping of hardware resources) currently consists of one provisioned [t2.micro EC2](https://aws.amazon.com/ec2/instance-types/t2/) instance. Both the backend and frontend containers run on this EC2 instance.

### Configurations

