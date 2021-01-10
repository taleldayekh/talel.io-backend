![CI](https://github.com/taleldayekh/talel.io-backend/workflows/CI/badge.svg) ![CD](https://github.com/taleldayekh/talel.io-backend/workflows/CD/badge.svg) [![codecov](https://codecov.io/gh/taleldayekh/talel.io-backend/branch/develop/graph/badge.svg)](https://codecov.io/gh/taleldayekh/talel.io-backend)

# Table of Contents

- [Architecture](#architecture)
  - [Architecture Layers](#architecture-layers)
- [API](#api)
- [Development](#development)
  - [Setup](#setup)
  - [Code Style](#code-style)
  - [Testing](#testing)
  - [CI/CD](#cicd)
- [Deployment](#deployment)
  - [Infrastructure Diagram](#infrastructure-diagram)
  - [Infrastructure Setup](#infrastructure-setup)
  - [AWS EC2](#aws-ec2-elastic-computing)
    - [NGINX](#nginx)
    - [Gunicorn](#gunicorn)
    - [Flask](#flask)

# Architecture

## Architecture Layers

```
╭──────────────────────╮
│  Presentation Layer  │
╰──────────────────────╯
           │
           │
           ▼
╭──────────────────────╮
│ Business Logic Layer │
╰──────────────────────╯
           ▲
	   │
	   │
╭──────────────────────╮
│    Database Layer    │
╰──────────────────────╯
```

# API

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

3. **Install dependencies**  

   ```bash
   pipenv install --dev
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

The **talel.io backend** consists of dockerized services for the NGINX web server, REST API and database which gets deployed to AWS and runs on a EC2 instance.

All services are defined in the [`docker-compose.yml`](./docker-compose.yml) file which automates the running of multiple containers with different configurations.

## Infrastructure Diagram

```
╭─── GitHub ───╮         ╭─── AWS ECR ───╮         ╭─── AWS ECS ───╮ API req ╭──────────────╮
│              │         │               │         │╭─────────────╮│ ◄────── │              │
│ Server CI/CD │ ──────► │ Server Images │ ──────► ││     EC2     ││         │ www.talel.io │
│              │         │               │         │╰─────────────╯│ ──────► │              │
╰──────────────╯         ╰───────────────╯         ╰───────────────╯ API res ╰──────────────╯
```

## Infrastructure Setup

1. **GitHub**  

   TXT

2. **AWS ECR (Elastic Container Registry)**  

   ECR is the Docker image repository on AWS. Each image has its separate repository holding different versions of a given image. For **talel.io backend** the repositories are:

   - talel.io-backend
   - nginx

   **Push Docker Image to ECR**

   To push a local Docker image, select a repository and click **View push commands**. This will bring up all necessary steps and commands for authenticating, taging and pushing a local Docker image.

   > The talel.io-backend and nginx images are automatically pushed to ECR in the CD pipeline.

   **Configurations**

   The **Lifecycle Policy** for each repository is set to only keep the latest version of an image.

3. **AWS ECS (Elastic Container Service)**  

   TXT

## AWS EC2 (Elastic Computing)

```
   ╭────────────────╮
   │                │
   │  www.talel.io  │
   │                │
   ╰────────────────╯
    Req           ▲
     │            │
     │            │  
     ▼           Res 
╭──── EC2 Instance ────╮
│ ╭───── Docker ─────╮ │
│ │╭────────────────╮│ │
│ ││      NGINX     ││ │
│ │╰────────────────╯│ │
│ ╰──────────────────╯ │
│           ▲          │
│           │          │
│           ▼          │
│ ╭───── Docker ─────╮ │
│ │╭────────────────╮│ │
│ ││    Gunicorn    ││ │
│ │╰────────────────╯│ │
│ │         ▲        │ │
│ │	    │        │ │
│ │         ▼        │ │
│ │╭────────────────╮│ │
│ ││ Flask REST API ││ │
│ │╰────────────────╯│ │
│ ╰──────────────────╯ │
╰──────────────────────╯
```

### NGINX

TXT

### Gunicorn

The Flask built in web server is meant for development only and is not suitable for handling concurrent requests in production. For production, a [Gunicorn WSGI application server](https://github.com/benoitc/gunicorn) is used to serve the Flask REST API service Python code.

Gunicorn runs behind NGINX.

### Flask

TXT





<!-- ```

## AWS ECR (Elastic Container Registry)

The Docker image artifacts which represents the application backend and frontend are hosted with [Amazon Elastic Container Registry](https://aws.amazon.com/ecr/).

Each image has its separate repository containing all versions of a given image. The lifecycle policy for the repositories is however set to only keep the latest version of an image.

## AWS ECS (Elastic Container Service)

[Amazon Elastic Container Service](https://aws.amazon.com/ecs/) orchestration platform manages and deploys Docker containers based on the images from the ECR.

The _*talelio*_ ECS cluster (grouping of hardware resources) currently consists of one provisioned [t2.micro EC2](https://aws.amazon.com/ec2/instance-types/t2/) instance. Both the backend and frontend containers run on this EC2 instance.

### Configurations -->
