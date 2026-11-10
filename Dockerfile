
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install application dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user and writable data directory
RUN groupadd --system cloudops \
    && useradd --system --gid cloudops cloudops \
    && mkdir /data \
    && chown cloudops:cloudops /data

# Copy the application
COPY app/ ./app/

USER cloudops

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.main:app", \
     "--host", "0.0.0.0", "--port", "8000"]
