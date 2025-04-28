FROM python:3.12-slim

WORKDIR /app

# Copy pyproject.toml first to leverage Docker cache
COPY pyproject.toml .

# Install build dependencies and project dependencies
RUN pip install --no-cache-dir .

# Copy the application code
COPY . .

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose the port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]