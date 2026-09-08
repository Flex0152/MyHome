FROM python:3.12-slim

WORKDIR /app

COPY app/ .
COPY pyproject.toml README.md ./

RUN pip install --no-cache-dir .

EXPOSE 8081

CMD ["python3", "main.py"]