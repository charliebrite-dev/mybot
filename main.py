import os
import random
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
MEME_FOLDER = "memes"

app = Flask(__name__)
telegram_app = Application.builder().token(TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Напиши /meme, чтобы получить мем 😎"
    )


async def meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    files = os.listdir(MEME_FOLDER)

    if not files:
        await update.message.reply_text("Мемов пока нет 😢")
        return

    file = random.choice(files)
    path = os.path.join(MEME_FOLDER, file)

    with open(path, "rb") as photo:
        await update.message.reply_photo(photo=photo)


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("meme", meme))


@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)
    return "ok"


@app.route("/")
def home():
    return "Bot is running 🚀"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
