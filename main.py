import os
import asyncio
from datetime import datetime
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

import shutil

if not shutil.which("ffmpeg"):
    raise RuntimeError("ffmpeg is not installed. Please install ffmpeg to continue.")

# Bot token'ınızı buraya girin
BOT_TOKEN = '7752492929:AAFe65OD0D3gh1QeaBc1crAacR8ttLSQ5JQ'

# İndirme klasörü oluştur
DOWNLOAD_DIR = 'downloads'
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

async def download_youtube(url):
    """YouTube videosunu indir"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(DOWNLOAD_DIR, f"youtube_{timestamp}.mp4")
        
        ydl_opts = {
            'format': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/mp4',
            'outtmpl': filename,
            'quiet': True,
            'no_warnings': True,
            'merge_output_format': 'mp4'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return filename
    except Exception as e:
        print(f"YouTube indirme hatası: {e}")
        return None

async def download_tiktok(url):
    """TikTok videosunu indir"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(DOWNLOAD_DIR, f"tiktok_{timestamp}.mp4")
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': filename,
            'quiet': True,
            'no_warnings': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        return filename
    except Exception as e:
        print(f"TikTok indirme hatası: {e}")
        return None

async def download_instagram(url):
    """Instagram videosunu indir"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(DOWNLOAD_DIR, f"instagram_{timestamp}.mp4")
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': filename,
            'quiet': True,
            'no_warnings': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        return filename
    except Exception as e:
        print(f"Instagram indirme hatası: {e}")
        return None

async def download_pinterest(url):
    """Pinterest görselini indir"""
    try:
        import aiohttp
        import re

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(DOWNLOAD_DIR, f"pinterest_{timestamp}.jpg")
        pin_id = url.split('/')[-2]  # Pinterest pin ID'sini al
        
        # Pinterest'in direkt resim URL yapısını kullan
        direct_url = f"https://i.pinimg.com/originals/{pin_id[:2]}/{pin_id[2:4]}/{pin_id[4:6]}/{pin_id}.jpg"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        
        async with aiohttp.ClientSession(headers=headers) as session:
            # Önce direkt URL'i dene
            async with session.get(direct_url) as response:
                if response.status == 200:
                    with open(filename, 'wb') as f:
                        f.write(await response.read())
                    return filename
                
            # Direkt URL başarısız olursa, sayfadan bul
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    
                    # Pinterest'in özel resim URL'lerini arama
                    patterns = [
                        r'https://i\.pinimg\.com/originals/[a-zA-Z0-9_/-]+\.(?:jpg|jpeg|png|webp)',
                        r'<meta property="og:image" content="([^"]+)"',
                        r'<link rel="image_src" href="([^"]+)"',
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, html)
                        if matches:
                            image_urls = []
                            for match in matches:
                                if isinstance(match, tuple):
                                    image_urls.extend(list(match))
                                else:
                                    image_urls.append(match)
                            
                            image_urls = [url for url in image_urls if url.startswith('http')]
                            if image_urls:
                                image_url = max(image_urls, key=len)
                                
                                async with session.get(image_url) as img_response:
                                    if img_response.status == 200:
                                        with open(filename, 'wb') as f:
                                            f.write(await img_response.read())
                                        return filename
        
        print("Pinterest içeriği bulunamadı")
        return None
        
    except Exception as e:
        print(f"Pinterest indirme hatası: {str(e)}")
        return None

async def start_command(update: Update, context):
    """Bot başlatma komutu"""
    await update.message.reply_text(
        'Merhaba! Ben bir sosyal medya indirme botuyum.\n'
        'YouTube, Instagram, TikTok veya Pinterest linkini gönder, '
        'ben de sana medyayı indirip göndereyim!'
    )

async def help_command(update: Update, context):
    """Yardım komutu"""
    await update.message.reply_text(
        'Desteklenen platformlar:\n'
        '- YouTube\n'
        '- Instagram\n'
        '- TikTok\n'
        '- Pinterest\n\n'
        'Kullanım: Sadece linki gönder!'
    )

async def handle_message(update: Update, context):
    """Mesaj işleme fonksiyonu"""
    url = update.message.text.strip()
    
    # Desteklenen platformları kontrol et
    if not any(domain in url.lower() for domain in ['youtube.com', 'youtu.be', 'instagram.com', 'tiktok.com', 'pinterest.com']):
        return

    try:
        # İndirme durumu mesajı gönder
        status_message = await update.message.reply_text("İndirme başlatılıyor...")
        
        # URL'nin platformuna göre indirme fonksiyonunu seç
        filename = None
        if 'youtube.com' in url or 'youtu.be' in url:
            filename = await download_youtube(url)
        elif 'instagram.com' in url:
            filename = await download_instagram(url)
        elif 'tiktok.com' in url:
            filename = await download_tiktok(url)
        elif 'pinterest.com' in url:
            filename = await download_pinterest(url)

        # Dosyayı gönder ve geçici dosyayı sil
        if filename and os.path.exists(filename):
            await update.message.reply_document(document=filename)
            os.remove(filename)
            await status_message.delete()
        else:
            await status_message.edit_text("İndirme başarısız oldu!")
    
    except Exception as e:
        await status_message.edit_text(f"Bir hata oluştu: {str(e)}")

def main():
    """Bot'u başlat"""
    # Bot uygulamasını oluştur
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Komut ve mesaj işleyicileri ekle
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Bot'u çalıştır
    print("Bot başlatılıyor...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()