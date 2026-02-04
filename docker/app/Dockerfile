FROM python:3.11-slim

WORKDIR /app

# Sistem paketlerini yükle
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# pip'i güncelle
RUN pip install --upgrade pip setuptools wheel

# Python paketlerini yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulamayı kopyala
COPY . .

# Streamlit portunu expose et
EXPOSE 8501

# Streamlit komutunu çalıştır
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
