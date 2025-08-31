# Telegram Meme Bot (Fly.io-ready)

Телеграм-бот, который присылает добрые мемы 💞. Работает 24/7 на Fly.io.

## Файлы
- bot.py — код бота
- requirements.txt — зависимости
- Dockerfile — образ для Fly.io
- fly.toml — конфиг Fly.io
- memes/ — папка с мемами
- .gitignore — исключает .env и прочее

## Деплой на Fly.io

1. Установи flyctl:
   ```bash
   # macOS
   brew install flyctl
   # или универсально (mac/linux)
   curl -L https://fly.io/install.sh | sh
   ```
2. Войти в Fly:
   ```bash
   fly auth login
   ```
3. Создать приложение (в директории с репо):
   ```bash
   fly launch --name telegram-meme-bot --no-deploy
   ```
4. (Опционально) создать volume для мемов, если хочешь добавлять их после деплоя:
   ```bash
   fly volumes create memes_data --size 1
   # и прописать mounts в fly.toml
   ```
5. Задать секреты:
   ```bash
   fly secrets set BOT_TOKEN="ВАШ_ТОКЕН" MEME_FOLDER="/app/memes"
   ```
6. Деплой:
   ```bash
   fly deploy
   ```
7. Смотреть логи:
   ```bash
   fly logs -a telegram-meme-bot
   ```

## Мемы
- Поддерживаются: .jpg, .jpeg, .png, .gif, .webp
- Подписи через __ в имени файла: cat__милота.png → подпись "милота"

## Важно
- Никогда не пушь BOT_TOKEN в репо. Используй secrets Fly.io.
