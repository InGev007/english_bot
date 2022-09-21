from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import translators as ts
import os
import time
import asyncio
import aioschedule

import keyboard as kb
import func
import dbutil
import bot_message
import tts
import bot_dictionary

bot= Bot(token=os.environ.get('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def command_start(message : types.Message):
    if message.from_user.is_bot != True:
        user=[message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.from_user.language_code]
        func.createuser(user)
        func.undolearn(message.from_id)
        await message.answer("Данный бот создан для изучения Английского языка. В нём вы найдете автоматический словарь который поможет вам запомнить основные слова. Набор правил анлийского языка и переводчик.", reply_markup=kb.startmenu)
        await message.delete()
        return
@dp.message_handler(commands=['msg'])
async def command_msg(message : types.Message):
    if message.from_user.is_bot != True:
        msg = message.text.strip('/msg ')
        await bot_message.send_msg(bot, msg, message.from_id, message)
        return
@dp.message_handler(commands=['message'])
async def command_msg(message : types.Message):
    if message.from_user.is_bot != True:
        msg = message.text.strip('/message ')
        await bot_message.send_msg(bot, msg, message.from_id, message)
        return
@dp.message_handler(commands=['update_voice'])
async def command_msg(message : types.Message):
    if message.from_user.is_bot != True:
        await tts.checkandupdatevoice(bot, message.from_id)
        return
@dp.message_handler(commands=['random'])
async def command_msg(message : types.Message):
    if message.from_user.is_bot != True:
        await tts.send_random(bot, message.from_id)
        return


@dp.message_handler()
async def echo_send(message : types.Message):
    if message.from_user.is_bot != True:
        user=[message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.from_user.language_code]
        state = func.checkstate(user)
        if state==0:
            if message.text=='Учить слова':
                func.setstate(message.from_id, 1)
                await message.delete()
                # text="Тебе необходимо переводить слова. Будет 4 варианта ответа. Слово считается выученным при правильном ответе 5 раз подряд для новых слов и 1 раз для уже выученных. За 1 урок 50 слов. Мы считаем это нормой для 1 дня учёбы. Завтра мы напомним тебе о необходимости продолжить учёбу. Твои результаты мы будем хранить 3дня. Если ты за 3 дня нам не напишешь мы удалим твой прогресс."
                # await bot.send_message(message.from_id, text)
                await bot_dictionary.startlearn(bot, message)
                return
            if message.text=='Переводчик':
                func.setstate(message.from_id, 2)
                await message.answer("Выбери с какого языка на какой переводим", reply_markup=kb.perevodmenu0)
                await message.delete()
                return
            if message.text=='Грамматика*(в разработке)':
                await message.delete()
                return
        elif state==1:
            if message.text=='Назад':
                func.setstate(message.from_id, 0)
                func.undolearn(message.from_id)
                await message.answer("Данный бот создан для изучения Английского языка. В нём вы найдете автоматический словарь который поможет вам запомнить основные слова. Набор правил анлийского языка и переводчик.", reply_markup=kb.startmenu)
                await message.delete()
                return
            else:
                await bot_dictionary.nextlearn(bot, message)
                return
        elif state==2:
            if message.text=='Англо-Русский':
                func.setstate(message.from_id, 3)
                await message.answer("Введите сообщение для перевода")
                await message.delete()
                return
            if message.text=='Руско-Английский':
                func.setstate(message.from_id, 4)
                await message.answer("Введите сообщение для перевода")
                await message.delete()
                return
            else:
                func.setstate(message.from_id, 0)
                await message.answer("Данный бот создан для изучения Английского языка. В нём вы найдете автоматический словарь который поможет вам запомнить основные слова. Набор правил анлийского языка и переводчик.", reply_markup=kb.startmenu)
                await message.delete()
                return
        elif state==3:
            answ = ts.google(message.text, to_language='ru')
            func.setstate(message.from_id, 2)
            await message.answer(answ, reply_markup=kb.perevodmenu0)
            await message.delete()
            return
        elif state==4:
            answ = ts.google(message.text, to_language='en')
            func.setstate(message.from_id, 2)
            await message.answer(answ, reply_markup=kb.perevodmenu0)
            await message.delete()
            return


async def setup_bot_commands():
    bot_commands = [
        types.BotCommand(command="/start", description="Для сброса и возвращения в главное меню"),
        types.BotCommand(command="/random", description="Случайное слово"),
    ]
    await bot.set_my_commands(bot_commands)

async def scheduler():
    aioschedule.every(1).minutes.do(send)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(_):
    dbutil.checkandupdatedb()
    await setup_bot_commands()
    # await bot_message.send_msg(bot, "У нас новая версия v0.2\nЧто нового:\n -Добавлено произношение слов\n -Добавлена новая комманда")
    asyncio.create_task(scheduler())

async def send():
    await bot_message.reminders(bot)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    
