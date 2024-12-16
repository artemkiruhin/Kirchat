import config
import telebot
import gpt_requests

bot = telebot.TeleBot(config.bot_token, parse_mode=None)
bot_messages = []

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    clear_button = telebot.types.InlineKeyboardButton("Очистить чат", callback_data='clear_chat')
    help_button = telebot.types.InlineKeyboardButton("Помощь", callback_data='show_help')
    markup.row(clear_button, help_button)

    welcome_message = ("Привет! Я бот с поддержкой GPT-4. "
                       "Просто отправьте мне сообщение, и я постараюсь ответить.")
    sent_message = bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

    bot_messages.append(message.message_id)
    bot_messages.append(sent_message.message_id)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'clear_chat':
        clear_chat(call.message)
        bot.answer_callback_query(call.id, "Чат очищен")
    elif call.data == 'show_help':
        help_message = (
            "tg: @glamfuneral\n"
            "github: https://github.com/artemkiruhin/Kirchat"
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, help_message)


def clear_chat(message):
    chat_id = message.chat.id
    for msg_id in bot_messages:
        try:
            bot.delete_message(chat_id, msg_id)
        except Exception as e:
            print(f"Не удалось удалить сообщение с ID {msg_id}: {e}")

    bot_messages.clear()


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    gpt_response = gpt_requests.get_gpt_response(message.text)

    markup = telebot.types.InlineKeyboardMarkup()
    clear_button = telebot.types.InlineKeyboardButton("Очистить чат", callback_data='clear_chat')
    help_button = telebot.types.InlineKeyboardButton("Помощь", callback_data='show_help')
    markup.row(clear_button, help_button)

    response = bot.reply_to(message, gpt_response, reply_markup=markup)

    bot_messages.append(message.message_id)
    bot_messages.append(response.message_id)


bot.infinity_polling()