FROM python:3.11-slim

#system-dependencies minimal
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

#requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#app-code
COPY app.py .

#standard gradio port
EXPOSE 7860

#lang for keywords
ENV KW_LANG=en

CMD ["python", "app.py"]
