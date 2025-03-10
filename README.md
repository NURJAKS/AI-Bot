# AI Telegram Bot

Этот бот использует AI для ответов в Telegram.

## 🚀 Установка

1. Установите Python 3.10

2. Клонируйте репозиторий: git clone https://github.com/NURJAKS/AI-Bot.git --> cd AI-Bot

3. Установите зависимости: "pip install -r requirements.txt"

4. Создайте `.env` и добавьте туда токены: "BOT_TOKEN=ваш*токен*бота" и "OPENROUTER_API_KEY=ваш*ключ_API"

5.Создайте файл "config.py" в папке с ботом и добавьте в него код:

import os 1
from dotenv import load_dotenv 2

load_dotenv() 3

BOT_TOKEN = os.getenv("BOT_TOKEN") 4
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") 5

6. Запустите бота: "python bot.py" 
