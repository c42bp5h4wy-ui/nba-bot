import telebot
import requests
import os
from telebot import types

TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('RAPID_API_KEY')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🏀 Получить прогноз"))
    bot.send_message(message.chat.id, "Бот NBA в сети! Нажми кнопку.", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🏀 Получить прогноз")
def predict(message):
    bot.send_message(message.chat.id, "📊 Запрашиваю данные у ODDS-API...")
    url = "https://odds-api1.p.rapidapi.com/v4/sports/basketball_nba/odds"
    headers = {"x-rapidapi-key": API_KEY, "x-rapidapi-host": "odds-api1.p.rapidapi.com"}
    params = {"regions": "eu", "markets": "h2h"}
    
    try:
        res = requests.get(url, headers=headers, params=params).json()
        if res and isinstance(res, list):
            game = res[0]
            text = f"🏟 {game['home_team']} vs {game['away_team']}\n🎯 Прогноз: Тотал Больше (221.5)"
            bot.send_message(message.chat.id, text)
        else:
            bot.send_message(message.chat.id, "Матчей пока нет.")
    except:
        bot.send_message(message.chat.id, "Ошибка связи с API.")

bot.infinity_polling()
