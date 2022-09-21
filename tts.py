import sqlite3
from gtts import gTTS
import os
from aiogram import Bot, types
from aiogram.types import InputFile
import dbutil
import random

async def checkandupdatevoice(bot, idu):
  con = sqlite3.connect("./db/bot.db")
  cur = con.cursor()
  res = cur.execute('SELECT id FROM admin WHERE id=%s'% idu)
  res = res.fetchall()
  if len(res)==0:
      await bot.send_message(idu, "У Вас нет досупа.")
      con.close()
      return
  res = cur.execute('UPDATE dictionary SET voice=NULL')
  con.commit()
  res = cur.execute('SELECT id, en FROM dictionary WHERE voice is NULL')
  res = res.fetchall()
  if len(res)!=0:
    for word in res:
      mytext = word[1]
      idd = word[0]
      language = 'en'
      myobj = gTTS(text=mytext, lang=language, slow=False)
      try:
          myobj.save("./speech/%s.mp3"%idd)
      except:
          os.mkdir('speech')
      finally:
          myobj.save("./speech/%s.mp3"%idd)

      voice = InputFile("./speech/%s.mp3"%idd)
      voice_send = await bot.send_voice(chat_id=idu, voice=voice, caption=mytext)
      voice_id = voice_send['voice']['file_id']
      sql = cur.execute('UPDATE dictionary SET voice="%s" WHERE id=%s;'% (voice_id,idd))
      con.commit()
  await bot.send_message(idu, "База данных озвучки - обновлена.")
  dbutil.dumpdb()
  con.close()

async def send_random(bot, idu):
    con = sqlite3.connect("./db/bot.db")
    cur = con.cursor()
    res = cur.execute('SELECT en,ru,transcription,voice FROM dictionary')
    dictionary = res.fetchall()
    con.close()
    random.shuffle(dictionary)
    if dictionary[0][2]==None: 
      await bot.send_voice(chat_id=idu, voice=dictionary[0][3], caption=dictionary[0][0]+" - "+dictionary[0][1])
    else:
      await bot.send_voice(chat_id=idu, voice=dictionary[0][3], caption=dictionary[0][0]+" ["+dictionary[0][2]+"] - "+dictionary[0][1])
