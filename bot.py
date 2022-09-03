from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os
import sqlite3

db.start()
bot= Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start','help','info'])
async def command_start(message : types.Message):
    await bot.send_message(message.from_id, dialog.start(comm_name, message.from_id))
    await message.delete()
    return
    
@dp.message_handler()
async def echo_send(message : types.Message):
    return



executor.start_polling(dp, skip_updates=True) 