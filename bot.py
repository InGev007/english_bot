from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import translators as ts
import os
import time

import keyboard as kb
import func

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
@dp.message_handler()
async def echo_send(message : types.Message):
    if (int(time.strftime("%H"))>9)&(int(time.strftime("%H"))<21):
        notactive=func.checkactive(message.from_id)
        if len(notactive)!=0:
            try:
                for e in notactive:
                    func.setstate(e[0], 0)
                    func.undolearn(e[0])
                    bot.send_message(e[0], "Продолжай изучать и повторять слова для успешного запоминания.", reply_markup=kb.startmenu)
            except: pass
    if message.from_user.is_bot != True:
        user=[message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, message.from_user.language_code]
        state = func.checkstate(user)
        if state==0:
            if message.text=='Учить слова':
                func.setstate(message.from_id, 1)
                word=func.startlearn(message.from_id)
                text="Тебе необходимо переводить слова. Будет 4 варианта ответа. Слово считается выученным при правильном ответе 5 раз подряд для новых слов и 1 раз для уже выученных. За 1 урок 50 слов. Мы считаем это нормой для 1 дня учёбы. Завтра мы напомним тебе о необходимости продолжить учёбу. Твои результаты мы будем хранить 3дня. Если ты за 3 дня нам не напишешь мы удалим твой прогресс."
                await message.answer(text)
                if word[5]==None:
                    await message.answer("Как переводится: %s"% word[4], reply_markup=kb.learnword(word))
                else:
                    await message.answer("Как переводится: %s [%s]"%(word[4],word[5]), reply_markup=kb.learnword(word))
                await message.delete()
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
                text,answ = func.nextlearn(message.from_id, message.text)
                if answ==0:
                    await message.answer(text, reply_markup=kb.startmenu)
                else:
                    await message.answer(text, reply_markup=kb.learnword(answ))
                await message.delete()
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

executor.start_polling(dp, skip_updates=True) 