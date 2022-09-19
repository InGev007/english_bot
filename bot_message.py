from aiogram import Bot, types
import sqlite3
import asyncio
import time

import func
import keyboard as kb

remtime=86400

async def reminders(bot):
    if (int(time.strftime("%H"))>9)&(int(time.strftime("%H"))<21):
        times=time.time()
        con = sqlite3.connect("./db/bot.db")
        cur = con.cursor()
        res = cur.execute('SELECT id,lastactive,lastsend FROM users')
        res = res.fetchall()
        users=[]
        if len(res)!=0:
            for user in res:
                if user[2]==0:
                    if (user[1]<=times-remtime):
                        users.append(user[0])
                else:
                    if (user[1]<=times-remtime)&(user[2]<=times-remtime):
                        users.append(user[0])
        if len(users)!=0:
            try:
                for idu in users:
                    func.setstate(idu, 0)
                    func.undolearn(idu)
                    await bot.send_message(idu, "Продолжай изучать и повторять слова для успешного запоминания.", reply_markup=kb.startmenu)
                    res = cur.execute('UPDATE users SET lastsend=%s WHERE id=%s;'% (times, idu))
                    con.commit()
            except Exception as error: print(error)
        con.close()
        users.clear()

async def send_msg(bot, msg, idu=None, message=None):
    con = sqlite3.connect("./db/bot.db")
    cur = con.cursor()
    if idu!=None:
        res = cur.execute('SELECT id FROM admin WHERE id=%s'% idu)
        res = res.fetchall()
        if len(res)==0:
            await bot.send_message(idu, "У Вас нет досупа.")
            if message!=None:
                await message.delete()
        else:
            res = cur.execute('SELECT id FROM users')
            res = res.fetchall()
            if len(res)!=0:
                for user in res:
                    await bot.send_message(user[0], msg)
                if message!=None:
                    await bot.send_message(idu, "Сообщение отправлено.")
                    await message.delete()
    else:
        res = cur.execute('SELECT id FROM users')
        res = res.fetchall()
        if len(res)!=0:
            for user in res:
                await bot.send_message(user[0], msg)
    con.close()
    return