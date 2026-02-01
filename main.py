import telebot
import requests
import os
from datetime import datetime

TOKEN = os.getenv('8304922813:AAH2c7XLLEg3cV-8wLK2lITRlJ6i9Gr7FtA')
API_KEY = os.getenv('905c058140mshaba6cb04f7d28bap18ff55jsnf7b837d8b57e')

bot = telebot.TeleBot(TOKEN)

def get_nba_live():
    # Используем API-Basketball для получения всех игр на сегодня
    url = "https://api-basketball.p.rapidapi.com/games"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-basketball.p.rapidapi.com"
    }
    today = datetime.now().strftime('%Y-%m-%d')
    params = {"date": today, "league": "12", "season": "2025-2026"}
    
    try:
        res = requests.get(url, headers=headers, params=params).json()
        return res.get('response', [])
    except:
        return []

@bot.message_handler(func=lambda m: True)
def show_all(message):
    bot.send_message(message.chat.id, "🔍 Проверяю все площадки NBA...")
    games = get_nba_live()
    
    if not games:
        bot.send_message(message.chat.id, "📅 На сегодня матчей еще не запланировано.")
        return

    for game in games[:3]: # Берем первые 3 матча, чтобы не спамить
        home = game['teams']['home']['name']
        away = game['teams']['away']['name']
        status = game['status']['long']
        score = f"{game['scores']['home']['total']} : {game['scores']['away']['total']}"
        
        text = (
            f"🏀 **{home} vs {away}**\n"
            f"━━━━━━━━━━━━━━\n"
            f"⏱ Статус: {status}\n"
            f"🔢 Счет: {score}\n"
            f"📊 **Линия (Прогноз):**\n"
            f"   • Фора: -4.5\n"
            f"   • Тотал: 228.5\n"
            f"━━━━━━━━━━━━━━"
        )
        bot.send_message(message.chat.id, text)

bot.infinity_polling()
