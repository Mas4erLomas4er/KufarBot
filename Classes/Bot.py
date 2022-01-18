import asyncio
import telebot

import config
from Classes.Watcher import Watcher


class Bot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.watchers = dict()

        self.bot.message_handler(commands=['start'])(self.start_cmd)
        self.bot.message_handler(commands=['set'])(self.set_cmd)
        self.bot.message_handler(commands=['stop'])(self.stop_cmd)

        self.bot.polling(none_stop=True)

    def start_cmd(self, user_msg):
        self.bot.send_message(
            user_msg.chat.id,
            'Hello! Welcome to Kufar Bot!\nYou can follow the updates of your favourite categories for FREE!'
        )
        self.bot.send_message(user_msg.chat.id, 'If you want to start, type /set')

    def set_cmd(self, user_msg):
        if user_msg.chat.id in self.watchers:
            self.bot.send_message(user_msg.chat.id, 'You have already started the process!')
            return

        self.bot.send_message(user_msg.chat.id, 'Please, enter the URL of the request:')

        self.bot.message_handler(func=lambda message: True)(self.set_url)

    def stop_cmd(self, user_msg):
        if user_msg.chat.id not in self.watchers:
            self.bot.send_message(user_msg.chat.id, 'You haven\'t got any processes!')
        else:
            self.watchers[user_msg.chat.id].stop_watching()
            self.watchers.pop(user_msg.chat.id)
            self.bot.send_message(user_msg.chat.id, 'Session stopped!', parse_mode='html')

    def set_url(self, user_msg):
        if user_msg.chat.id in self.watchers:
            self.bot.send_message(user_msg.chat.id, 'You have already started the process!')
            return
        self.watchers[user_msg.chat.id] = Watcher(user_msg.text, self.event(user_msg.chat.id))
        self.bot.send_message(user_msg.chat.id, 'Watching for YOU!')
        asyncio.run(self.watchers[user_msg.chat.id].start_watching(config.INTERVAL))

    def event(self, chat_id):
        def print_result(msg):
            self.bot.send_message(chat_id, msg)
        return print_result
