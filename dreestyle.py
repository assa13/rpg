from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import requests

# Вставьте ваши токены
TELEGRAM_TOKEN = "7669075260:AAGQRvjP05Zhdh2iW2ZhUwFEjzcR4r2mQy8"
HUGGINGFACE_API_TOKEN = "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"

# URL API Hugging Face
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/gpt2"

# Функция для получения ответа от Hugging Face
def query_huggingface(prompt):
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
    payload = {"inputs": prompt}
    response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]["generated_text"]
    else:
        return "Ошибка генерации ответа."

# Команда /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я бот, который отвечает на вопросы и может общаться.")

# Обработка текстовых сообщений
async def handle_message(update: Update, context):
    user_message = update.message.text
    bot_response = query_huggingface(user_message)
    await update.message.reply_text(bot_response)

def main():
    # Создаем приложение Telegram
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    app.run_polling()

if __name__ == "__main__":
    main()
