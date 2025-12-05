# Haftalık Raporlayıcı Telegram Botu

Bu bot, kullanıcıdan haftalık rapor bilgilerini ister ve Google Gemini ile Türkçe özet üretir.

## Gerekli Ortam Değişkenleri
- `TELEGRAM_BOT_TOKEN`: BotFather'dan aldığınız Telegram bot token'ı.
- `GOOGLE_GEMINI_API_KEY`: Gemini API anahtarınız.

## Kurulum
1. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements-telegram.txt
   ```
2. Ortam değişkenlerini ayarlayın:
   ```bash
   export TELEGRAM_BOT_TOKEN="<telegram_token>"
   export GOOGLE_GEMINI_API_KEY="<gemini_api_key>"
   ```

## Çalıştırma
Botu başlatmak için proje dizininde:
```bash
python telegram_bot.py
```
Telegram'da botunuza `/start` yazarak soruları yanıtlayın. Rapor özeti otomatik olarak oluşturulur.
