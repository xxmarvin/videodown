# Python tabanlı hafif bir Docker imajı kullan
FROM python:3.9-slim

# Gerekli sistem bağımlılıklarını yükle (ffmpeg dahil)
RUN apt-get update && apt-get install -y ffmpeg curl && apt-get clean

# Çalışma dizini oluştur
WORKDIR /app

# Python bağımlılıklarını yüklemek için dosyaları kopyala
COPY requirements.txt .

# Python bağımlılıklarını yükle
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY main.py .

# Bot'u çalıştır
CMD ["python", "main.py"]