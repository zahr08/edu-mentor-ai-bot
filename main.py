import os
import telebot
from openai import OpenAI
from dotenv import load_dotenv

# .env fayldagi TOKEN va API key ni yuklaymiz
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Telegram bot va OpenAI client
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

# /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🎓 Assalomu alaykum!\nEdu Mentor AI ga xush kelibsiz.\n"
        "Savolingizni yozing va men sizga tushunarli tarzda javob beraman."
    )

# Foydalanuvchi xabarini AI orqali javoblash
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an educational AI mentor. Explain simply."},
            {"role": "user", "content": message.text}
        ]
    )
    answer = response.choices[0].message.content
    bot.send_message(message.chat.id, answer)

# Botni ishga tushiramiz
bot.polling()
