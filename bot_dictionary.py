import sqlite3
import random
import time
from aiogram import Bot, types
import keyboard as kb
import func


def randansw():
    con = sqlite3.connect("./db/bot.db")
    cur = con.cursor()
    i1=list(range(1, 1000))
    random.shuffle(i1)
    res = con.execute('SELECT ru FROM dictionary WHERE id in (%s,%s,%s)'% (i1[0],i1[1],i1[2]))
    res=res.fetchall()
    answ=[res[0][0],res[1][0],res[2][0]]
    con.close()
    return answ

async def startlearn(bot, message):
    uid=message.from_id
    text="Тебе необходимо переводить слова. Будет 4 варианта ответа. Слово считается выученным при правильном ответе 5 раз подряд для новых слов и 1 раз для уже выученных. За 1 урок 50 слов. Мы считаем это нормой для 1 дня учёбы. Завтра мы напомним тебе о необходимости продолжить учёбу. Твои результаты мы будем хранить 3дня. Если ты за 3 дня нам не напишешь мы удалим твой прогресс."
    await bot.send_message(uid, text)
    con = sqlite3.connect("./db/bot.db")
    cur = con.cursor()
    res = con.execute('SELECT id FROM dictionary WHERE id NOT IN (SELECT idd FROM tempdict WHERE idu=%s);'% uid)
    res=res.fetchall()
    coll=len(res)
    answ=res
    random.shuffle(answ)
    if coll!=0:
        i=0
        while i<50:
            try:
                res = con.execute('INSERT INTO tempdict (idu,idd) VALUES (%s,%s);'% (uid,answ[i][0]))
                con.commit()
            except:
                pass
            i+=1
    answ=randansw()
    res = con.execute('SELECT en,ru,id,transcription,voice FROM dictionary WHERE id IN (SELECT idd FROM tempdict WHERE idu=%s);'% uid)
    res=res.fetchall()
    random.shuffle(res)
    answ.append(res[0][1])
    sql = con.execute('INSERT INTO t_dial (idu,ganswer,idd) VALUES (%s,"%s",%s);'% (uid,answ[3],res[0][2]))
    con.commit()
    random.shuffle(answ)
    answ.append(res[0][0])
    answ.append(res[0][3])
    answ.append(res[0][4])
    con.close()
    if answ[5]==None:
        #await message.answer("Как переводится: %s"% answ[4], reply_markup=kb.learnword(answ))
        await bot.send_voice(chat_id=uid, voice=answ[6], caption="Как переводится: " + answ[4], reply_markup=kb.learnword(answ))
    else:
        #await message.answer("Как переводится: %s [%s]"%(answ[4],answ[5]), reply_markup=kb.learnword(answ))
        await bot.send_voice(chat_id=uid, voice=answ[6], caption="Как переводится: " + answ[4] + " [" + answ[5] +"]", reply_markup=kb.learnword(answ))
    return answ

async def nextlearn(bot, message):
    uid=message.from_id
    text=message.text
    await message.delete()
    con = sqlite3.connect("./db/bot.db")
    cur = con.cursor()
    res = con.execute('SELECT ganswer,idd FROM t_dial WHERE idu=%s;'% uid)
    res=res.fetchone()
    answ=res
    res = con.execute('DELETE FROM t_dial WHERE idu=%s;'% uid)
    con.commit()
    idd=answ[1]
    if answ[0]==text:
        res = con.execute('UPDATE tempdict SET good=good+1, wrong=0, ok= CASE WHEN (ok=0 AND good = 2) OR (ok=1) THEN 1 ELSE 0 END WHERE idd=%s AND idu=%s;'% (idd,uid))
        ret="Правильный ответ. Следующие слово: "
    else:
        res = con.execute('UPDATE tempdict SET good=0,wrong=1 WHERE idd=%s AND idu=%s;'% (idd,uid))
        ret = "Неправильно. Правильный ответ: " + answ[0] + ". Следующие слово: "
    con.commit()
    res = con.execute('SELECT idd FROM tempdict WHERE idu=%s AND ((good<2 AND ok=0)OR(good=0 AND ok=1));'%uid)
    res=res.fetchall()
    tempdict=res
    coll=len(tempdict)
    if coll==0:
        func.setstate(uid,0)
        res = con.execute('UPDATE tempdict SET good=0, wrong=0, ok=1 WHERE idu=%s'%uid)
        ret = "Ты успешно выучил ещё 50 слов. Продолжай в том-же духе и помни перерыв в обучении сведёт весь успех к нулю."
        con.commit()
        con.close()
        await bot.send_message(uid, ret, reply_markup=kb.startmenu)
        return
    else:
        random.shuffle(tempdict)
        res = con.execute('SELECT en,ru,id,transcription,voice FROM dictionary WHERE id=%s;'% tempdict[0][0])
        res=res.fetchone()
        if (text==res[1])&(coll!=1):
            res = con.execute('SELECT en,ru,id,transcription,voice FROM dictionary WHERE id=%s;'% tempdict[1][0])
            res=res.fetchone()
        answ=randansw()
        answ.append(res[1])
        sql = con.execute('INSERT INTO t_dial (idu,ganswer,idd) VALUES (%s,"%s",%s);'% (uid,answ[3],res[2]))
        con.commit()
        random.shuffle(answ)
        con.close()
        if res[3]==None:
            ret=ret+res[0]
        else:
            ret=ret+res[0]+" ["+res[3]+"]"
        await bot.send_voice(chat_id=uid, voice=res[4], caption=ret, reply_markup=kb.learnword(answ))
        return