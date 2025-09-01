FROM python:3.10-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY requirements.txt requirements-dev.txt ./

# Install dependencies
RUN uv pip install --system --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ ./src/

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
