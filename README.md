# Haftalık Raporlayıcı Telegram Botu

Telegram üzerinden haftalık rapor toplar, Google Gemini ile özetler ve kullanıcıya sunar.

## Gereksinimler
- Python 3.10+
- Bir Telegram bot token'ı (BotFather ile oluşturabilirsiniz)
- Google Gemini API anahtarı (https://aistudio.google.com)

## Kurulum Adımları
1. Depo dizinine geçin ve bağımlılıkları kurun:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Gerekli ortam değişkenlerini tanımlayın (örnek `.env` içeriği):
   ```bash
   export TELEGRAM_BOT_TOKEN="<telegram-bot-token>"
   export GOOGLE_GEMINI_API_KEY="<gemini-api-key>"
   ```
   > Google anahtarı tanımlanmazsa bot yine çalışır, ancak özet basit metin olarak döner.
3. Botu başlatın:
   ```bash
   python telegram_bot.py
   ```
4. Telegram'da botunuza `/start` yazın ve gelen soruları sırayla yanıtlayın.

## Çalışma Akışı
1. Bot tarih aralığını sorar.
2. Bu hafta yapılan işleri alır.
3. Tamamlananları ister.
4. Gelecek hafta planını alır.
5. Risk/engel var mı diye sorar.
6. Gemini ile özeti üretir ve kullanıcıya gönderir.

## Özelleştirme
- Soruları veya ek alanları `bots/weekly_report_bot.py` içindeki `ConversationHandler` sırasını değiştirerek ekleyebilirsiniz.
- Prompt'u `_build_summary_prompt` fonksiyonunda özelleştirerek farklı özet formatları üretebilirsiniz.

## Geliştirme
- Kod `python-telegram-bot` (v20) üzerinde asenkron çalışır.
- Özetleme Google Gemini ("gemini-1.5-flash") modeliyle yapılır; farklı model için `_configure_gemini` fonksiyonunu güncelleyin.
>>>>>>> theirs
