import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
import os

# .env faylni yuklash
load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

bot = telebot.TeleBot(API_TOKEN)
user_states = {}

# Menyu funksiyalari
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("📩 Savol yuborish"))
    markup.row(KeyboardButton("🌐 Mening saytlarim"))
    return markup

def sites_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("GitLab"), KeyboardButton("GitHub"))
    markup.row(KeyboardButton("YouTube"), KeyboardButton("Instagram"))
    markup.row(KeyboardButton("Telegram"), KeyboardButton("⬅️ Orqaga"))
    return markup

@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    user_states[user_id] = "idle"
    bot.send_message(
        message.chat.id,
        "👋 Salom! Menga savolingiz bo‘lsa, marhamat!",
        reply_markup=main_menu()
    )

@bot.message_handler(commands=['getchatid'])
def get_chat_id(message):
    bot.send_message(message.chat.id, f"🆔 Chat ID: {message.chat.id}")

@bot.message_handler(content_types=['text'])
def text_handler(message):
    user_id = message.from_user.id
    text = message.text.strip().lower()

    if text == "📩 savol yuborish":
        user_states[user_id] = "waiting_for_question"
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row(KeyboardButton("⬅️ Bekor qilish"))
        bot.send_message(
            message.chat.id,
            "✍️ Savolingizni yozing. Uni admin ga yuboraman.",
            reply_markup=markup
        )
    elif text == "🌐 mening saytlarim":
        bot.send_message(
            message.chat.id,
            "🌐 Mening saytlarim 👇",
            reply_markup=sites_menu()
        )
    elif text in ["gitlab", "github", "youtube", "instagram", "telegram"]:
        links = {
            "gitlab": "https://gitlab.com/UzJaFaR-13",
            "github": "https://github.com/UzJaFaR-13",
            "youtube": "https://youtube.com",
            "instagram": "https://instagram.com/uzjafar_13/",
            "telegram": "https://t.me/UzJaFaR_13"
        }
        bot.send_message(
            message.chat.id,
            f"{text.capitalize()}: {links[text]}",
            reply_markup=sites_menu()
        )
    elif text in ["⬅️ orqaga", "⬅️ bekor qilish"]:
        user_states[user_id] = "idle"
        bot.send_message(
            message.chat.id,
            "🔙 Asosiy menyuga qaytdingiz.",
            reply_markup=main_menu()
        )
    elif user_states.get(user_id) == "waiting_for_question":
        first_name = message.from_user.first_name or "Nomaʼlum"
        username = f"@{message.from_user.username}" if message.from_user.username else "yoʻq"
        bot.send_message(
            ADMIN_CHAT_ID,
            f"📥 Yangi savol:\n"
            f"👤 Ism: {first_name}\n"
            f"💬 Username: {username}\n"
            f"🆔 ID: {user_id}\n\n"
            f"📩 Savol:\n{message.text}"
        )
        bot.send_message(
            message.chat.id,
            "✅ Savolingiz yuborildi! Tez orada javob beraman.",
            reply_markup=main_menu()
        )
        user_states[user_id] = "idle"
    else:
        bot.send_message(
            message.chat.id,
            "Iltimos, tugmalardan foydalaning yoki savol yuboring. 😊",
            reply_markup=main_menu()
        )

bot.infinity_polling()
