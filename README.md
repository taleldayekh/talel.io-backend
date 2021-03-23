![CI](https://github.com/taleldayekh/talel.io-backend/workflows/CI/badge.svg) ![CD](https://github.com/taleldayekh/talel.io-backend/workflows/CD/badge.svg) [![codecov](https://codecov.io/gh/taleldayekh/talel.io-backend/branch/develop/graph/badge.svg)](https://codecov.io/gh/taleldayekh/talel.io-backend)

# Table of Contents

- [Architecture](#architecture)
  - [Architecture Layers Overview](#architecture-layers-overview)
  - [Presentation Layer](#presentation-layer)
  - [Business Logic Layer](#business-logic-layer)
  - [Data Layer](#data-layer)
- [API](#api)
  - [Account Resource Overview](#account-resource-overview)
  - [Account Resource Details](#account-resource-details)
- [Database Schema Migration](#database-schema-migration)
- [Development](#development)
  - [Setup](#setup)
  - [Code Style](#code-style)
  - [Testing](#testing)
  - [CI/CD](#cicd)
- [Deployment](#deployment)
  - [Infrastructure Diagram](#infrastructure-diagram)
  - [Deployment Stack](#deployment-stack)
    - [GitHub](#github)
    - [AWS ECR](#aws-ecr-elastic-container-registry)
    - [AWS ECS](#aws-ecs-elastic-container-service)
    - [AWS EC2](#aws-ec2-elastic-computing)
      - [AWS Elastic IP and Namecheap DNS](#aws-elastic-ip-and-namecheap-dns)
      - [Traefik Reverse Proxy](#traefik-reverse-proxy)
      - [Gunicorn](#gunicorn)
      - [Flask](#flask)
      - [PostgreSQL DB](postgresql-db)

# Architecture

Describe DDD

## Architecture Layers Overview

Diagram of Architecture

## Presentation Layer

Description of Presentation Layer

## Business Logic Layer

Description of Business Logic Layer

## Data Layer

### Folder Structure

```
└── talelio_backend/
    └── data/
    ╵   └── orm.py
    ╵   └── repositories.py
    ╵   └── uow.py
```

### Repositories

The repositories provides an abstraction over the data storage. They decouple the business logic layer from the database and allows for retrieving and storing domain model data while hiding database access details.

The repositories collaborates with a **Unit of Work** (uow) which groups any database related functions and executes them as an _*atomic*_ unit. This is done in a context manager where all changes either gets saved to the database or rolled back if anything fails.

The uow is initialized by the API in the interface layer and passed to use-cases in the service layer.

### ORMs

[SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) is used as the ORM (object relational mapper) that keeps the domain models database agnostic and not dependent on any particular database technology. By keeping the models ignorant of the persistence storage the database can easily be switched at any point in time.

SQLAlchemy helps define schemas, map them to domain models and generate SQL based on the model objects.

### Database

# API

Details about the REST API

## Account Resource Overview

| HTTP Method | Description          | Resource                               | Success Code | Failure Code |
|-------------|----------------------|----------------------------------------|--------------|--------------|
| POST        | Account registration | /\<version\>/accounts/register         | 201          | 400          |
| GET         | Verified account     | /\<version\>/accounts/verify/\<token\> | 200          | 400          |

## Account Resource Details

<details>
<summary>POST account registration</summary>

<br/>

⚠️ Endpoint for registering account can only be successfully queried if email is included in whitelisted emails.

### Request

```bash
curl -X POST \
https://api.talel.io/v1/accounts/register \
-H "Content-Type: application/json" \
-d '{"email": <str>, "password": <str>, "username": <str>}'
```

### Success Response

```bash
201: CREATED

{
  "id": <int>,
  "created_at": <str>,
  "updated_at": <str>,
  "verified": <bool>,
  "email": <str>,
  "user": {
    "id": <int>,
    "username" <str>,
    "location" <str>,
    "avatar_url": <str>
  }
}
```

### Error Response

```bash
400: BAD REQUEST

{
  "error": {
    "message": "expected '<key>' key",
    "status": 400,
    "type": "Bad Request"
  }
}
```

```bash
400: BAD REQUEST

{
  "error": {
    "message": "Email not whitelisted",
    "status": 400,
    "type": "Bad Request"
  }
}
```

```bash
400: BAD REQUEST

{
  "error": {
    "message": "Account with the '<email>' email already exists",
    "status": 400,
    "type": "Bad Request"
  }
}
```
</details>

<details>
<summary>GET verified account</summary>

### Request

```bash
curl -X GET \
https://api.talel.io/v1/accounts/verify/<token>
```

### Success Response

```bash
200: OK

{
  "id": <int>,
  "created_at": <str>,
  "updated_at": <str>,
  "verified": <bool>,
  "email": <str>,
  "user": {
    "id": <int>,
    "username": <str>,
    "location": <str>,
    "avatar_url": <str>
  }
}
```

### Error Response

```bash
400: BAD REQUEST

{
  "error": {
    "message": "No registered account with the email '<email>'",
    "status": 400,
    "type": "Bad Request"
  }
}
```

```bash
400: BAD REQUEST

{
  "error": {
    "message": "Account already verified",
    "status": 400,
    "type": "Bad Request"
  }
}
```
</details>

# Database Schema Migration

Database migrations is handled with [Alembic](https://github.com/sqlalchemy/alembic).

Run Alembic in the command line whenever a model has been created or modified. This will generate a Python migration script which can be invoked to upgrade the database schema.

1. **Auto-generate migration script**

   ```bash
   alembic revision --autogenerate -m "<message>"
   ```

2. **Perform migration**  

   ```bash
   alembic upgrade head
   ```

Above steps will auto-generate necessary SQL for transforming the database into the new version.





<!-- Architecture

## Architecture Layers


```
          Presentation Layer
          ╭── Business Logic Layer ──╮
	  │ ╭──────────────────────╮ │
	  │ │       Use Case       │ │
	  │ ╰──────────────────────╯ │
	  │ ╭──────────────────────╮ │
     +	  │ │     Domain Model     │ │
     |	  │ ╰──────────────────────╯ │
     |	  ╰──────────────────────────╯
     |
     |    ╭─────── Data Layer ───────╮
     |    │ ╭──────────────────────╮ │
     |    │ │     Repositories     │ │
     |    │ ╰──────────────────────╯ │
     |    │ ╭──────────────────────╮ │
     +----+ │         ORMs         │ │ 
          │ ╰──────────────────────╯ │
          │ ╭──────────────────────╮ │
          │ │       Database       │ │
          │ ╰──────────────────────╯ │
          ╰──────────────────────────╯
```

### Data Layer -->





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

## Deployment Stack

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
   ╭─────────────────╮
   │                 │
   │ talel.io client │
   │                 │
   ╰─────────────────╯
       Req ↓ ↑ Res
╭───────────────────── EC2 ─────────────────────╮
│ ╭──── Container ────╮                         │
│ │╭─────────────────╮│                         │
│ ││ Traefik Reverse ││                         │
│ ││      Proxy      ││                         │
│ │╰─────────────────╯│                         │
│ ╰───────────────────╯                         │
│          ↓ ↑                                  │
│ ╭──── Container ────╮                         │
│ │╭─────────────────╮│                         │
│ ││  Gunicorn WSGI  ││                         │
│ ││   HTTP Server   ││   ╭──── Container ────╮ │
│ │╰─────────────────╯│   │╭─────────────────╮│ │
│ │        ↓ ↑        │ ← ││  PostgreSQL DB  ││ │
│ │╭─────────────────╮│ → ││                 ││ │
│ ││  Flask RESTful  ││   │╰─────────────────╯│ │
│ ││       API       ││   ╰───────────────────╯ │
│ │╰─────────────────╯│                         │
│ ╰───────────────────╯                         │
╰───────────────────────────────────────────────╯
```

The following configurations needs to be considered for a working deployment setup on the EC2 instance.

### AWS Elastic IP and Namecheap DNS

The DNS connects the various `www.talel.io` / `talel.io` domain and subdomains with IP addresses.

The **talel.io API** can be accessed via the subdomain `api.talel.io` which is connected to the EC2 instance with a static IP provided by **AWS Elastic IP**.

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

   - Create a new **A Record** for the various hosts, i.e. `www` for `www.talel.io` and `api` for `api.talel.io`.

   - Add the Elastic IP for the EC2 instance as **Value** for all relevant records.

   > An A Record (Address Record) directs the domain to a server through its IPv4 address and controls what a domain name does when visited.

### PostgreSQL DB

The PostgreSQL container runs as an ECS Service with a mounted volume for persisting the db on the EC2 host.

**Configurations**

The directory in the container where PostgreSQL stores its data needs to be bind mounted in the ECS Task Definition.

- In the `postgresql-task` Task Definition, scroll down to **Volumes** and click on **Add volume**.

- Enter **talelio-postgresql** as **Name**.

- Enter `/var/lib/talelio-postgresql` as **Source path**, this will be the location of the db on the EC2 host.

- Under **Container Definitions** click on the **postgresql-container** and scroll down to **STORAGE AND LOGGING**.

- Select **talelio-postgresql** as **Source volume**.

- Enter `/var/lib/postgresql/data` as **Container path**, this is the path in the container where PostgreSQL creates the db.

### Traefik Reverse Proxy





When a request is made to `api.talel.io` [Traefik](https://github.com/traefik/traefik) acts as a reverse proxy and redirects that request to the Flask REST API service served by Gunicorn.

Traefik forwards everything over `HTTPS` and only exposes ports `80` and `443` for `HTTP` and `HTTPS` respectively as well as port `8080` for the built in [dashboard](https://doc.traefik.io/traefik/operations/dashboard/).

**Configurations**

The Traefik dockerized task runs as a service on the **talelio cluster**. It is not included in the CD pipeline as it is not expected to be redeployed frequently.

Any service that is deployed on ECS and configured with the correct Docker labels will automatically get picked up by Traefik.

> The Traefik [static](/traefik/traefik.toml) and [dynamic](/traefik/traefik_dynamic.toml) configuration files are well-commented.

1. **Traefik Static Configurations**  

   These configurations are set once when the container is launched and in addition to specifying ports and HTTPS forwarding this is also where the ECS provider and TLS certificate generation is defined.

   - **ECS Provider**  

     Enables the use of Traefik in a ECS cluster.

   - **TLS with Let's Encrypt**  

     In the configurations a **Certificate Resolver** is defined which retrives a certificate and enables TLS for a domain. This happens when a **router** in the dynamic configurations requests a certificate for a domain.

     Certificates are automatically renewed.

     > ⚠️ If the `caServer` staging server was used for generating test certificates, generating production certificates might fail unless the files created during testing are manually deleted from the host.

2. **Traefik Dynamic Configurations**  

   TXT

### Gunicorn

The Flask built in web server is meant for development only and is not suitable for handling concurrent requests in production. For production, a [Gunicorn WSGI application server](https://github.com/benoitc/gunicorn) is used to serve the Flask REST API service Python code.

Gunicorn runs behind NGINX.

### Flask

TXT





<!-- ```

## AWS ECR (Elastic Container Registry)

The Docker image artifacts which represents the application backend and frontend are hosted with [Amazon Elastic Container Registry](https://aws.amazon.com/ecr/).

### Configurations -->
