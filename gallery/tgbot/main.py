import os
import time
import telebot
import datetime
from threading import Thread
from django.conf import settings

from gallery.tgbot.filters import filters
from gallery.tgbot.orders import get_data, process_order

bot = telebot.TeleBot(settings.BOT_TOKEN)
chat_id = settings.CHAT_ID
dbname = settings.DATABASES['default']['NAME']
user = settings.DATABASES['default']['USER']
password = settings.DATABASES['default']['PASSWORD']
host = settings.DATABASES['default']['HOST']


def main():
    print(os.environ)


# custom filters
filters(bot, chat_id)


# initializes work of the bot
@bot.message_handler(is_group=True, is_admin=True, commands=['start'])
def start(message):
    print(type(message.chat.id))
    print(f"Bot has been initialized in '{bot.get_chat(message.chat.id).title}' chat")
    bot.send_message(message.chat.id, 'Добрый день!')
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    orders_btn = telebot.types.KeyboardButton('📋Заказы')
    markup.add(orders_btn)

    bot.send_message(message.chat.id, 'Нажмите "📋Заказы", чтобы посмотреть список заказов.', reply_markup=markup)


# gets orders with status='pending'
@bot.message_handler(is_group=True, is_admin=True, content_types=['text'])
def orders(message='📋Заказы'):
    if message.text == '📋Заказы':
        get_data(
                 chat_id=chat_id,
                 bot=bot
                 )


# calls inline button click handler function
@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
    process_order(call=call,
                  bot=bot,
                  chat_id=chat_id,
                  )


# tracks membership of the bot in the groups
@bot.my_chat_member_handler()
def chat_status(message):
    print(f'Someone has added/removed your bot')
    print(f'Name of the group: {bot.get_chat(message.chat.id).title}')
    print(f'ID of the chat: {message.chat.id}')


# gets automatically list of orders every 10 minutes
def auto_bot():
    ten_minutes = 600
    while True:
        get_data(
            chat_id=chat_id,
            bot=bot
        )
        time.sleep(ten_minutes)


def main():
    print(f"Connection started: {datetime.datetime.now().strftime('%B %d %Y %H:%M')}")

    # runs concurrently auto queries of "pending" orders and polling
    thread1 = Thread(target=auto_bot)
    thread2 = Thread(target=bot.infinity_polling)
    thread1.start()
    thread2.start()






