# Proposal of API project (WIP)

The goal of this project architecture is to meet Palenca's main development pain points


## Must include
- Clean Architecture
- Docker
- FastAPI
- Pydantic (Models and validations)
- Tortoise ORM (Async)
- Migrations Aerich
- OpenAPI generator using FastAPI for easy doc management
- Sandbox environment
- Testing
- Logger
- Timing Middleware
- Sentry integration
- Webhook example
- Detect Plaform Downtime or response changes
- Tasks (Celery)

## Steps to run the project

```bash
docker build -t palenca_core -f Dockerfile.development .
docker run -it -v "$(pwd)":/opt/api:cached -p 9000:9000 palenca_core /bin/bash -l
python -m api.app
```

## Run tests

```bash
docker exec -it CONTAINER_ID /bin/bash -l
pytest -n auto --timeout=5

```

## Run coverage

```bash
docker exec -it CONTAINER_ID /bin/bash -l
pytest --cov-report term-missing --cov=api

```