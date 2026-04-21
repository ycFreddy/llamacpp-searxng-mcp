FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    gcc libxml2-dev libxslt1-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY serveur.py .
EXPOSE 8000
CMD ["python", "serveur.py"]