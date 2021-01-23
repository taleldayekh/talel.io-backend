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
  - [Deployment Setup](#deployment-setup)
    - [GitHub](#github)
    - [AWS ECR](#aws-ecr-elastic-container-registry)
    - [AWS ECS](#aws-ecs-elastic-container-service)
  - [AWS EC2](#aws-ec2-elastic-computing)
    - [AWS Elastic IP and Namecheap DNS](#aws-elastic-ip-and-namecheap-dns)
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

The **talel.io backend** consists of dockerized services for the NGINX web server and the REST API which are deployed to AWS in the CD pipeline and runs on a EC2 instance.

All services in the deployment setup can also be run locally with `docker-compose`:

```bash
docker-compose build
docker-compose up
```

## Infrastructure Diagram

```
╭─── GitHub ───╮         ╭─── AWS ECR ───╮         ╭─── AWS ECS ───╮ API req ╭──────────────╮
│              │         │               │         │╭─────────────╮│ ◄────── │              │
│ Server CI/CD │ ──────► │ Server Images │ ──────► ││     EC2     ││         │ www.talel.io │
│              │         │               │         │╰─────────────╯│ ──────► │              │
╰──────────────╯         ╰───────────────╯         ╰───────────────╯ API res ╰──────────────╯
```

## Deployment Setup

### GitHub

TXT

### AWS ECR (Elastic Container Registry)

[ECR](https://aws.amazon.com/ecr/) is the Docker image repository on AWS. Each image has a separate repository with different versions of the given image.

The repositories for the **talel.io backend** are:

- **talel.io-backend**
- **nginx**

**Push local Docker image to ECR**

Select a repository and click **View push commands**. This will bring up all necessary steps and commands for authenticating, tagging and pushing a local Docker image.

> The **talel.io-backend** and **nginx** images are automatically pushed to ECR in the CD pipeline.

**Configurations**

The **Lifecycle Policy** for each repository is set to keep only the latest version of an image.

### AWS ECS (Elastic Container Service)

[ECS](https://aws.amazon.com/ecs/) is the orchestration platform on AWS which manages and deploys Docker containers based on the images from ECR.

ECS is configured with the three main components: _*cluster*_, _*task definition*_ and _*service*_.

1. **Cluster (grouping of hardware resources)**  

   The entire backend lies on the **talelio** ECS cluster which currently consists of one provisioned [t2.micro EC2](https://aws.amazon.com/ec2/instance-type/t2/) instance. Both the **talel.io-backend** and **nginx** container runs on this EC2 instance.

   **Configurations**

   The **talelio** cluster has been setup with the following configurations:

   TXT

2. **Task definition**  

   The task definition is a template for how a Docker container gets deployed to the EC2 instance. The **talelio** cluster have two task definitions, a [talelio-backend-task](.aws/talelio-backend-task-definition.json) and a [nginx-task](.aws/nginx-task-definition.json).

3. **Service**  

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
╭───────────────── EC2 Instance ─────────────────╮
│ ╭───── Docker ─────╮      ╭───── Docker ─────╮ │
│ │╭────────────────╮│      │╭────────────────╮│ │
│ ││      NGINX     ││ ◄─── ││ SSL w/ Certbot ││ │
│ │╰────────────────╯│      │╰────────────────╯│ │
│ ╰──────────────────╯      ╰──────────────────╯ │
│         ▲  ▲                       ▲           │
│         │  │                       │           │
│         │  │                       ▼           │
│         │  ╰──────────────────► Volumes        │
│         ▼                                      │
│ ╭───── Docker ─────╮                           │
│ │╭────────────────╮│                           │
│ ││    Gunicorn    ││                           │
│ │╰────────────────╯│                           │
│ │         ▲        │                           │
│ │         │        │                           │
│ │         ▼        │                           │
│ │╭────────────────╮│                           │
│ ││ Flask REST API ││                           │
│ │╰────────────────╯│                           │
│ ╰──────────────────╯                           │
╰────────────────────────────────────────────────╯
```

The following configurations needs to be considered for a working deployment setup with EC2.

### AWS Elastic IP and Namecheap DNS

The DNS connects the various **www.talel.io** / **talel.io** domain and subdomains with IP addresses.

The **talel.io API** can be accessed via the subdomain **api.talel.io** which is connected to the EC2 instance with a static IP provided by **AWS Elastic IP**.

**Configurations**

1. **AWS Elastic IP**  

   - Navigate to **EC2** -> **Network & Security** -> **Elastic IPs**.

   - Click to **Allocate Elastic IP address**.

   - Make sure **Amazon's pool of IPv4 addresses** is selected and click **Allocate**.

   - Click on **Associate this Elastic IP address** to bind the Elastic IP address with an EC2 instance.

   - Select the relevant EC2 instance and click **Associate**.

   > An Elastic IP address is free of charge as long as **only that address** is associated with one running EC2 instance.

2. **Namecheap DNS**  

   The **talel.io** domain is registered on [Namecheap](https://www.namecheap.com) and the DNS settings on Namecheap needs to be adjusted to point to the EC2 instance.

   - From **Domain List** click to manage the domain and select **Advanced DNS**.

   - Under **HOST RECORDS** click to **ADD NEW RECORD**.

   - Create a new **A Record** for the various hosts, i.e. `www` for **www.talel.io** and `api` for **api.talel.io**.

   - Add the Elastic IP for the EC2 instance as **Value** for all relevant records.

   > An A Record (Address Record) directs the domain to a server through its IPv4 address and controls what a domain name does when visited.



---

### NGINX

TXT

### SSL with Certbot

TXT - Elastic IP

### Gunicorn

The Flask built in web server is meant for development only and is not suitable for handling concurrent requests in production. For production, a [Gunicorn WSGI application server](https://github.com/benoitc/gunicorn) is used to serve the Flask REST API service Python code.

Gunicorn runs behind NGINX.

### Flask

TXT





<!-- ```

## AWS ECR (Elastic Container Registry)

The Docker image artifacts which represents the application backend and frontend are hosted with [Amazon Elastic Container Registry](https://aws.amazon.com/ecr/).

### Configurations -->
