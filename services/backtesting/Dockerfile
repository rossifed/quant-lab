FROM python:3.12-slim

WORKDIR /workspace

RUN pip install --no-cache-dir uv

COPY pyproject.toml .

COPY shared ./shared

COPY services/backtesting ./services/backtesting

RUN uv sync --all-packages --no-dev

ENV PYTHONPATH=/workspace

WORKDIR /workspace/services/backtesting

EXPOSE 8000

CMD ["uv", "run", "--directory", "/workspace", "uvicorn", "services.backtesting.main:app", "--host", "0.0.0.0", "--port", "8000"]
