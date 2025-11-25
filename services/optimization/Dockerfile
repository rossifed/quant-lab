FROM python:3.12-slim

WORKDIR /workspace

# Install uv only (Ray will be installed via pyproject.toml)
RUN pip install --no-cache-dir uv

COPY pyproject.toml .

COPY shared ./shared

COPY services/optimization ./services/optimization

RUN uv sync --all-packages --no-dev

ENV PYTHONPATH=/workspace
WORKDIR /workspace/services/optimization

EXPOSE 8000

CMD ["uv", "run", "--directory", "/workspace", "uvicorn", "services.optimization.main:app", "--host", "0.0.0.0", "--port", "8000"]