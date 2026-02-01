import telebot
import requests
import os
from telebot import types

TOKEN = os.getenv('BOT_TOKEN')
API_KEY = os.getenv('RAPID_API_KEY')

bot = telebot.TeleBot(TOKEN)

def get_full_odds():
    url = "https://odds-api1.p.rapidapi.com/v4/sports/basketball_nba/odds"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "odds-api1.p.rapidapi.com"
    }
    # Запрашиваем сразу все основные рынки: h2h (исход), totals (тотал), spreads (фора)
    params = {
        "regions": "eu",
        "markets": "h2h,totals,spreads",
        "oddsFormat": "decimal"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        return response.json()
    except:
        return []

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("🏀 Линия NBA"))
    bot.send_message(message.chat.id, "📊 Бот загружен. Нажми кнопку для получения полной линии с БК.", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🏀 Линия NBA")
def send_line(message):
    data = get_full_odds()
    if not data or not isinstance(data, list):
        bot.send_message(message.chat.id, "📭 На данный момент линия пуста.")
        return

    game = data[0] # Берем ближайший матч
    home = game['home_team']
    away = game['away_team']
    
    # Словари для хранения данных
    odds_info = {"h2h": "", "total": "", "spread": ""}
    
    # Ищем данные в ответе API (проходим по букмекерам)
    bookie = game['bookmakers'][0] # Берем коэффициенты первого букмекера в списке
    for market in bookie['markets']:
        if market['key'] == 'h2h':
            o = market['outcomes']
            odds_info["h2h"] = f"П1: {o[0]['price']} | П2: {o[1]['price']}"
        
        if market['key'] == 'totals':
            o = market['outcomes'][0]
            odds_info["total"] = f"Тотал {o['point']}: Б({o['price']})"
            
        if market['key'] == 'spreads':
            o = market['outcomes'][0]
            odds_info["spread"] = f"Фора {o['name']} ({o['point']}): {o['price']}"

    text = (
        f"🏀 **{home} vs {away}**\n"
        f"━━━━━━━━━━━━━━\n"
        f"✅ **Исход:** {odds_info['h2h']}\n"
        f"📈 **Фора:** {odds_info['spread']}\n"
        f"📊 **Тотал:** {odds_info['total']}\n"
        f"━━━━━━━━━━━━━━\n"
        f"🔥 *Данные обновлены из БК*"
    )
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

bot.infinity_polling()
