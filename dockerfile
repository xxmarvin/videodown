FROM python:3.9-slim

# Sistemi güncelle ve ffmpeg'i yükle
RUN apt-get update && apt-get install -y ffmpeg

# Gerekli bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ana dosyayı kopyala
COPY main.py .

# Çalıştırma komutu
CMD ["python", "main.py"]