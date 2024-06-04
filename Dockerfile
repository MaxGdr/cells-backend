FROM python:3.12-slim

# Fix poetry home & poetry version
ENV POETRY_VERSION=1.8.3 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME="/opt/poetry" \
  POETRY_NO_INTERACTION=1

RUN pip install poetry==$POETRY_VERSION

# Copy API Source code
COPY src src/
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-dev
WORKDIR /src
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]