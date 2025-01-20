# Temel Python görüntüsünü kullan
FROM python:3.10-slim

# FFmpeg'i kur
RUN apt-get update && apt-get install -y ffmpeg

# Çalışma dizinini ayarla
WORKDIR /app

# Gereksinim dosyalarını kopyala ve yükle
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Başlatma komutu
CMD ["python", "main.py"]