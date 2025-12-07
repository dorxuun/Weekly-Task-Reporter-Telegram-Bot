# 🤖 Haftalık Raporlayıcı Telegram Botu

Bu proje, Telegram üzerinden haftalık rapor verilerini toplayan, **Google Gemini (2.5 Flash)** ile özetleyen, oluşan özeti **DOCX dosyasına dönüştürüp Google Drive’a otomatik yükleyen** bir bottur.

---

## 🚀 Özellikler

- ✅ Telegram üzerinden adım adım haftalık rapor toplar  
- ✅ Google Gemini 2.5 Flash ile otomatik özet çıkarır  
- ✅ Sadece **Gemini özetini içeren DOCX** oluşturur  
- ✅ DOCX dosyasını **Google Drive’a otomatik yükler**  
- ✅ Drive linkini kullanıcıya Telegram’dan gönderir  
- ✅ Asenkron ve hızlı çalışır  

---

## 🛠 Gereksinimler

- Python **3.10+**
- Telegram Bot Token
- Google Gemini API Key
- Google Drive API için `credentials.json`

---

## 📦 Kurulum

### 1️⃣ Projeyi klonla
```bash
git clone https://github.com/dorxuun/Weekly-Task-Reporter-Telegram-Bot.git
cd Weekly-Task-Reporter-Telegram-Bot
```

### 2️⃣ Sanal ortam oluştur ve aktif et
```bash
python -m venv .venv
source .venv/bin/activate   # Mac / Linux
```

### 3️⃣ Gerekli kütüphaneleri kur
```bash
pip install -r requirements.txt
```

---

## 🔐 Ortam Değişkenleri (.env)

Proje kök dizinine `.env` dosyası oluştur ve şunları yaz:

```env
TELEGRAM_BOT_TOKEN=BURAYA_TELEGRAM_TOKEN
GOOGLE_GEMINI_API_KEY=BURAYA_GEMINI_API_KEY
```

---

## ☁️ Google Drive Bağlantısı

1. Google Cloud Console’dan **OAuth istemcisi oluştur**
2. `credentials.json` dosyasını proje kök dizinine koy
3. Bot ilk çalıştırıldığında tarayıcı açılır ve Google hesabından izin ister
4. Otomatik olarak `token.json` oluşturulur (**bu dosya gitignore’dadır, GitHub’a gitmez**)

---

## ▶️ Botu Çalıştırma

```bash
python telegram_bot.py
```

Telegram’da:

```
/start
```

---

## 🔄 Bot Akışı

1. 📅 Tarih aralığını sorar  
2. ✅ Bu hafta yapılanlar  
3. 📦 Tamamlanan işler  
4. 🗓 Haftaya yapılacaklar  
5. 🧠 Gemini özeti üretir  
6. 📄 DOCX oluşturur  
7. ☁️ Google Drive’a yükler  
8. 🔗 Drive linkini Telegram’dan gönderir  

---

## 📑 Oluşturulan DOCX İçeriği

DOCX dosyasında **sadece Gemini özeti bulunur**:

```
Haftalık Rapor Özeti

- Tarih Aralığı
- Öne Çıkanlar
- Tamamlananlar
- Önümüzdeki Hafta Planı
```

---

## 📂 Proje Yapısı

```
.
├── telegram_bot.py
├── gdrive_upload.py
├── requirements.txt
├── .env
├── credentials.json
├── .gitignore
└── README.md
```

---

## ⚠️ Güvenlik

- `token.json` kesinlikle GitHub’a gönderilmez
- `.gitignore` içinde otomatik engellenmiştir
- Yanlışlıkla gönderildiyse geçmiş temizlenmelidir

---

## 👨‍💻 Geliştirici

**dorxuun**

✅ Gemini 2.5 Flash aktiftir  
✅ DOCX çıktısı aktiftir  
✅ Google Drive yükleme aktiftir  
✅ Sistem tam çalışır durumdadır  
