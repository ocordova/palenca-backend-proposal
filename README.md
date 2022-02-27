## Steps to run the project

```bash
docker build -t palenca_core -f Dockerfile.development .
docker run -it -v "$(pwd)":/opt/api:cached -p 9000:9000 palenca_core /bin/bash -l
aerich upgrade # Run migrations
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
