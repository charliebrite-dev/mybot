import logging
import os
import random
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, ContextTypes, CallbackQueryHandler
)

load_dotenv()

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("meme-bot")

BOT_TOKEN = os.getenv("BOT_TOKEN")
MEME_FOLDER = os.getenv("MEME_FOLDER", "./memes")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Put it in environment or .env")

BUTTON_MEME = "meme_request"
keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Прислать мем", callback_data=BUTTON_MEME)]]
)

WELCOME_TEXT = "Привет! Я бот, который присылает добрые мемы 💞"

VALID_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

def _list_memes(folder: str):
    p = Path(folder)
    if not p.exists():
        return []
    return [f for f in p.iterdir() if f.is_file() and f.suffix.lower() in VALID_EXTS]

def _caption_from_name(path: Path) -> str | None:
    if "__" in path.stem:
        parts = path.stem.split("__", 1)
        cap = parts[1].replace("_", " ").strip()
        return cap if cap else None
    return None

async def send_random_meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    files = _list_memes(MEME_FOLDER)
    if not files:
        msg = (
            "Папка с мемами пустая 🤷‍♂️\n"
            f"Текущий путь: `{MEME_FOLDER}`"
        )
        if update.effective_message:
            await update.effective_message.reply_text(msg, parse_mode="Markdown")
        return

    path: Path = random.choice(files)
    caption = _caption_from_name(path)

    try:
        with open(path, "rb") as f:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=InputFile(f, filename=path.name),
                caption=caption
            )
    except Exception as e:
        logger.exception("Failed to send meme: %s", e)
        if update.effective_message:
            await update.effective_message.reply_text("Не смог отправить мем 😢")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_TEXT, reply_markup=keyboard)

async def meme_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_random_meme(update, context)

async def on_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == BUTTON_MEME:
        class U:
            effective_chat = update.effective_chat
            effective_message = query.message
        await send_random_meme(U, context)

def main():
    app = Application.builder().token(BOT_TOKEN).concurrent_updates(True).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("meme", meme_cmd))
    app.add_handler(CallbackQueryHandler(on_button))

    logger.info("Starting bot. MEME_FOLDER=%s", MEME_FOLDER)
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
