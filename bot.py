from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import keyboard as kb
import func

import os
import sqlite3

bot= Bot(token="5697881354:AAEleWp6gm-KZRsHLOH2a2kJQ0VU61xAxGQ")
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def command_start(message : types.Message):
    func.createuser(message.from_id)
    await message.answer("Данный бот создан для изучения Английского языка. В нём вы найдете автоматический словарь который поможет вам запомнить основные слова. Набор правил анлийского языка и переводчик.", reply_markup=kb.startmenu)
    await message.delete()
    
@dp.message_handler()
async def echo_send(message : types.Message):
    state = func.checkstate(message.from_id)
    if state==0:
        if message.text=='Учить слова':
            func.setstate(message.from_id, 1)
            word=func.startlearn(message.from_id)
            text="Тебе необходимо переводить слова. Будет 4 варианта ответа. Слово считается выученным при правильном ответе 5 раз подряд для новых слов и 1 раз для уже выученных. За 1 урок 50 слов. Мы считаем это нормой для 1 дня учёбы. Завтра мы напомним тебе о необходимости продолжить учёбу. Твои результаты мы будем хранить 3дня. Если ты за 3 дня нам не напишешь мы удалим твой прогресс."
            await message.answer(text)
            await message.answer("Как переводится: %s"% word[4], reply_markup=kb.learnword(word))
            await message.delete()
        return
    elif state==1:
        return
    await bot.send_message(message.from_id, message.text)
    await message.delete()


executor.start_polling(dp, skip_updates=True) 