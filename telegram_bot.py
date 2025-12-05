from dotenv import load_dotenv
load_dotenv()
import logging
import os
from typing import Dict

import google.generativeai as genai
from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (Application, CommandHandler, ConversationHandler,
                          ContextTypes, MessageHandler, filters)

ASK_DATE_RANGE, ASK_ACCOMPLISHMENTS, ASK_COMPLETED, ASK_NEXT_WEEK = range(4)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def configure_gemini(api_key: str) -> None:
    genai.configure(api_key=api_key)


def build_summary_prompt(responses: Dict[str, str]) -> str:
    date_range = responses.get("date_range", "")
    accomplishments = responses.get("accomplishments", "")
    completed = responses.get("completed", "")
    next_week = responses.get("next_week", "")

    return (
        "Sen bir takımın haftalık rapor yardımcısısın. "
        "Kullanıcıdan gelen bilgileri kısa, maddeler halinde ve Türkçe olarak özetle.\n\n"
        f"Tarih aralığı: {date_range}\n"
        "Bu hafta yapılanlar:\n"
        f"{accomplishments}\n\n"
        "Biten işler:\n"
        f"{completed}\n\n"
        "Haftaya yapılacaklar:\n"
        f"{next_week}\n\n"
        "Çıktıya aşağıdaki başlıklarla cevap ver:\n"
        "- Tarih Aralığı\n"
        "- Öne Çıkanlar\n"
        "- Tamamlananlar\n"
        "- Önümüzdeki Hafta Planı\n"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(
        "Merhaba! Haftalık raporunu oluşturmaya hazırım. "
        "Önce rapor için tarih aralığını girer misin?"
    )
    return ASK_DATE_RANGE


async def ask_accomplishments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["date_range"] = update.message.text
    await update.message.reply_text("Bu hafta neler yapıldı? Kısaca paylaşır mısın?")
    return ASK_ACCOMPLISHMENTS


async def ask_completed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["accomplishments"] = update.message.text
    await update.message.reply_text("Biten işler veya teslimatlar neler?")
    return ASK_COMPLETED


async def ask_next_week(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["completed"] = update.message.text
    await update.message.reply_text(
        "Haftaya hangi işleri yapmayı planlıyorsun? Kısa notlar bırakabilirsin."
    )
    return ASK_NEXT_WEEK


async def summarize_and_finish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["next_week"] = update.message.text

    gemini_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    if not gemini_key:
        await update.message.reply_text(
            "Özetlemek için GOOGLE_GEMINI_API_KEY ortam değişkenini ayarlaman gerekiyor.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END

    configure_gemini(gemini_key)
    prompt = build_summary_prompt(context.user_data)

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        summary = response.text.strip() if response and response.text else "Özet oluşturulamadı."
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Gemini isteği başarısız oldu: %s", exc)
        summary = "Özet oluşturulurken bir hata oluştu."

    await update.message.reply_text(summary, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(
        "İşlem iptal edildi. Yeniden başlamak için /start yazabilirsin.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def main() -> None:
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN ortam değişkeni ayarlanmalı.")

    application = Application.builder().token(bot_token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_DATE_RANGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_accomplishments)],
            ASK_ACCOMPLISHMENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_completed)],
            ASK_COMPLETED: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_next_week)],
            ASK_NEXT_WEEK: [MessageHandler(filters.TEXT & ~filters.COMMAND, summarize_and_finish)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("cancel", cancel))

    logger.info("Bot başlatıldı. Telegram üzerinden /start yazarak deneyebilirsin.")
    application.run_polling()


if __name__ == "__main__":
    main()
