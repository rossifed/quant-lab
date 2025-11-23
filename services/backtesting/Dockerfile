FROM python:3.12-slim

WORKDIR /workspace

# Install uv
RUN pip install --no-cache-dir uv

# Copy workspace root pyproject.toml
COPY pyproject.toml .

# Copy shared library
COPY shared ./shared

# Copy service files
COPY services/backtesting ./services/backtesting

# Install all workspace dependencies including service dependencies
RUN uv sync --all-packages --no-dev

# Set Python path and working directory
ENV PYTHONPATH=/workspace
WORKDIR /workspace/services/backtesting

# Expose port
EXPOSE 8000

# Run the service using uv from the service directory
CMD ["uv", "run", "--directory", "/workspace", "uvicorn", "services.backtesting.main:app", "--host", "0.0.0.0", "--port", "8000"]
