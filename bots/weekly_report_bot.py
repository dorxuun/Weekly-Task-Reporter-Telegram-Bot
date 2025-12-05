"""Telegram bot for collecting weekly reports and summarizing them with Gemini."""

import logging
import os
from textwrap import dedent
from typing import Dict, Optional

import google.generativeai as genai
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

DATE_RANGE, DONE_THIS_WEEK, COMPLETED_ITEMS, NEXT_WEEK_PLAN, BLOCKERS = range(5)
logger = logging.getLogger(__name__)


def _configure_gemini(api_key: Optional[str]) -> Optional[genai.GenerativeModel]:
    """Configure and return the Gemini model when an API key is available."""
    if not api_key:
        logger.warning("GOOGLE_API_KEY is not set; falling back to plain text summary.")
        return None

    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


def _build_summary_prompt(answers: Dict[str, str]) -> str:
    """Craft a concise prompt for Gemini using the collected answers."""
    return dedent(
        f"""
        Şu bilgileri haftalık bir durum raporuna dönüştür:
        - Tarih aralığı: {answers['date_range']}
        - Bu hafta neler yapıldı: {answers['done_this_week']}
        - Tamamlanan işler: {answers['completed_items']}
        - Haftaya planlananlar: {answers['next_week_plan']}
        - Riskler/engeller: {answers['blockers']}

        Beklenen çıktı:
        - 4-6 maddelik kısa bir özet
        - Net aksiyonlar ve sahipleri
        - Kritik riskler için kısa öneri
        - Türkçe, anlaşılır ve Telegram için biçimlendirilmiş
        """
    ).strip()


async def _summarize_with_gemini(answers: Dict[str, str]) -> str:
    """Summarize answers with Gemini, with a graceful fallback."""
    model = _configure_gemini(os.getenv("GOOGLE_API_KEY"))
    prompt = _build_summary_prompt(answers)

    if model is None:
        return dedent(
            f"""
            📅 Tarih: {answers['date_range']}
            ✅ Bu hafta: {answers['done_this_week']}
            🎯 Tamamlananlar: {answers['completed_items']}
            🔜 Haftaya: {answers['next_week_plan']}
            ⚠️ Riskler: {answers['blockers']}

            (Özet için GOOGLE_API_KEY tanımlayın.)
            """
        ).strip()

    response = model.generate_content(prompt)
    return response.text if response and response.text else "Özet oluşturulamadı."


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(
        "Merhaba! Haftalık rapor için birkaç soru soracağım. İstediğinde /cancel yazabilirsin.\n"
        "Lütfen tarih aralığını gir (ör. 1-5 Mayıs 2024)."
    )
    return DATE_RANGE


async def capture_date_range(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["date_range"] = update.message.text
    await update.message.reply_text("Bu hafta neler yapıldı?")
    return DONE_THIS_WEEK


async def capture_done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["done_this_week"] = update.message.text
    await update.message.reply_text("Tamamlanan işler neler?")
    return COMPLETED_ITEMS


async def capture_completed(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["completed_items"] = update.message.text
    await update.message.reply_text("Gelecek hafta neler yapacaksın?")
    return NEXT_WEEK_PLAN


async def capture_next_week(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["next_week_plan"] = update.message.text
    await update.message.reply_text("Riskler veya engeller var mı?")
    return BLOCKERS


async def capture_blockers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["blockers"] = update.message.text
    await update.message.reply_text("Özet hazırlanıyor, lütfen bekleyin…")

    summary = await _summarize_with_gemini(context.user_data)
    await update.message.reply_text(summary, reply_markup=ReplyKeyboardMarkup([ ["/start"] ], resize_keyboard=True))
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Raporlamayı iptal ettim. Yeni bir rapor için /start yaz.")
    return ConversationHandler.END


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN environment variable is required")

    app = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            DATE_RANGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, capture_date_range)],
            DONE_THIS_WEEK: [MessageHandler(filters.TEXT & ~filters.COMMAND, capture_done)],
            COMPLETED_ITEMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, capture_completed)],
            NEXT_WEEK_PLAN: [MessageHandler(filters.TEXT & ~filters.COMMAND, capture_next_week)],
            BLOCKERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, capture_blockers)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("cancel", cancel))

    logger.info("Bot is polling...")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
