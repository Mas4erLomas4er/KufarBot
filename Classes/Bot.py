import asyncio
import config
import logging
from aiogram import Bot as IOBot, Dispatcher, executor, types

from Classes import Async
from Classes.Watcher import Watcher


class Bot:
    def __init__(self, token):
        logging.basicConfig(level=logging.INFO)
        self.bot = IOBot(token=token)
        self.dp = Dispatcher(self.bot)
        self.watchers = dict()

        self.dp.message_handler(commands=['start'])(self.start_cmd)
        self.dp.message_handler(commands=['set'])(self.set_cmd)
        self.dp.message_handler(commands=['stop'])(self.stop_cmd)

        Async.loop.run_until_complete(executor.start_polling(self.dp, skip_updates=True))

    async def start_cmd(self, user_msg: types.Message):
        await user_msg.answer('Hello! Welcome to Kufar Bot!\nYou can follow the updates of your favourite categories for FREE!')
        await user_msg.answer('If you want to start, type /set')

    async def set_cmd(self, user_msg: types.Message):
        if user_msg.chat.id in self.watchers:
            await user_msg.answer('You have already started the process!')
            return

        await user_msg.answer('Please, enter the URL of the request:')
        self.dp.message_handler()(self.set_url)

    async def stop_cmd(self, user_msg: types.Message):
        if user_msg.chat.id not in self.watchers:
            await user_msg.answer('You haven\'t got any processes!')
        else:
            self.watchers[user_msg.chat.id].stop_watching()
            self.watchers.pop(user_msg.chat.id)
            await user_msg.answer('Session stopped!', parse_mode='html')

    async def set_url(self, user_msg: types.Message):
        if user_msg.chat.id in self.watchers:
            await user_msg.answer('You have already started the process!')
            return
        self.watchers[user_msg.chat.id] = Watcher(user_msg.text, self.event(user_msg))
        await user_msg.answer('Watching for YOU!')
        await self.watchers[user_msg.chat.id].start_watching()

    def event(self, user_msg: types.Message):
        async def print_result(msg):
            await user_msg.answer(msg)

        return print_result
