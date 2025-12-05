FROM python:3.9-slim

WORKDIR /app

COPY /app .

RUN mkdir -p /app/data

RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

EXPOSE 8000

CMD ["alembic", "upgrade", "head"]
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]