FROM python:3.10-slim

# Avoid Python buffering issues
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 7860
EXPOSE 8501

CMD ["bash", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 7860 & streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0"]
