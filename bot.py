import telebot
import requests
import sys
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not BOT_TOKEN or not OPENROUTER_API_KEY:
    raise ValueError("Missing environment variables!")
  

bot = telebot.TeleBot(BOT_TOKEN)

print("Бот запущен...") 

# Welcome message for the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = ("Welcome to the AI Chatbot! 🤖\n"
                    "Ask me anything.\n"
                    "To exit the chat, just type 'exit'.")
    bot.send_message(message.chat.id, welcome_text)

# Function to print streaming text in terminal
def print_streaming_text(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.005)  # Скорость вывода текста (можно менять)
    print()  # Переход на новую строку после завершения

session = requests.Session()  # Создаём глобальную сессию

def get_ai_response(text):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    
    json_data = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [{"role": "user", "content": text}],
        "temperature": 0.7,
        "top_p": 0.8
    }
    
    try:
        response = session.post(url, headers=headers, json=json_data, timeout=5)  # Добавил таймаут
        response.raise_for_status()  # Вызывает ошибку, если запрос не успешен
        bot_response = response.json().get('choices', [{}])[0].get('message', {}).get('content', '').strip()
        return bot_response if bot_response else "Я пока не знаю ответа 😕"
    except requests.exceptions.RequestException:
        return "Ошибка запроса 😔"


@bot.message_handler(func=lambda message: True)
def respond_to_message(message):
    user_message = message.text.strip()
    chat_id = message.chat.id
    
    print("Пользователь отправил:", user_message)  # Логируем входящее сообщение
    
    if user_message:  # Проверяем, что сообщение не пустое
        bot_response = get_ai_response(user_message)
    else:
        bot_response = "Я не понял ваш вопрос 🤔"
    
    # Проверяем длину ответа и отправляем частями, если нужно
    if len(bot_response) > 4000:
        for i in range(0, len(bot_response), 4000):
            bot.send_message(chat_id, bot_response[i:i+4000])
    else:
        bot.send_message(chat_id, bot_response)

# Start polling
bot.polling()
