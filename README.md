# 📝 Haftalık Raporlayıcı Telegram Botu

Telegram üzerinden kullanıcıdan haftalık iş bilgilerini toplayan ve Google Gemini’nin **gemini-2.5-flash** modeliyle özetleyen bir raporlama botudur.

---

## 🚀 Özellikler
- Tarih aralığı, yapılan işler, tamamlananlar, gelecek hafta planı gibi bilgileri toplar.
- Google Gemini ile **madde madde profesyonel haftalık rapor** üretir.
- \`python-telegram-bot\` (v20) ile tamamen **asenkron** çalışır.
- Kolay kurulum, kolay özelleştirme.

---

## 📦 Gereksinimler
- Python **3.10+**
- Telegram bot token (BotFather ile alınır)
- Google Gemini API key (https://aistudio.google.com)

---

## ⚙️ Kurulum

### 1. Sanal ortam oluştur & bağımlılıkları kur
\`\`\`bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
\`\`\`

### 2. Ortam değişkenlerini tanımla
\`\`\`bash
export TELEGRAM_BOT_TOKEN="<telegram-bot-token>"
export GOOGLE_GEMINI_API_KEY="<gemini-api-key>"
\`\`\`

> API key girilmezse bot çalışır ama özet kısmı normal metin olarak döner.

### 3. Botu başlat
\`\`\`bash
python telegram_bot.py
\`\`\`

### 4. Telegram’da \`/start\` yaz
Bot seni sırayla yönlendirecek.

---

## 🔄 Çalışma Akışı
1. Bot tarih aralığını sorar.
2. Bu hafta yapılan işleri alır.
3. Tamamlanan görevleri alır.
4. Gelecek hafta planını ister.
5. (Eğer kodda aktifse) risk/engel bilgisi alır.
6. Gemini ile **4–6 maddelik profesyonel özet** üretir.

---

## 🛠 Özelleştirme

### Soruları değiştirmek istiyorsan:
\`telegram_bot.py\` içindeki \`ConversationHandler\` akışını düzenle.

### Özet biçimini değiştirmek istiyorsan:
Gemini’ye gönderilen prompt’u düzenle:
\`\`\`python
_build_prompt()
\`\`\`

---

## 👨‍💻 Teknoloji Notları
- Bot \`python-telegram-bot\` v20 ile async mimaride çalışır.
- Varsayılan model: **gemini-2.5-flash**
- Modeli değiştirmek için:
\`\`\`python
model = genai.GenerativeModel("gemini-2.5-flash")
\`\`\`

---

## ✅ Hazırsın!
Artık botu çalıştırabilir, GitHub’a temiz şekilde pushlayabilir ve eklemeler yapabilirsin.
