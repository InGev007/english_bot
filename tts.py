import sqlite3
from gtts import gTTS
import os
from aiogram import Bot, types
from aiogram.types import InputFile

async def checkandupdatevoice(bot, idu):
  con = sqlite3.connect("./db/bot.db")
  cur = con.cursor()
  res = cur.execute('SELECT id, en FROM dictionary WHERE voice is NULL LIMIT 2')
  res = res.fetchall()
  if len(res)!=0:
    for word in row:
      mytext = word[1]
      idd = word[0]
      language = 'en'
      myobj = gTTS(text=mytext, lang=language, slow=False)
      myobj.save("./speech/%s.mp3"%idd)  
      try:
          myobj.save("./speech/%s.mp3"%idd)
      except:
          os.mkdir('speech')
      finally:
          myobj.save("./speech/%s.mp3"%idd)
      #voice = InputFile("./speech/%s.mp3"%mytext.replace("'", ""))
      voice = InputFile("./speech/%s.mp3"%idd)
      voice_send = await bot.send_audio(chat_id=idu, audio=voice, caption="текст1",title=mytext) # этот метод поможет получить file_id
      voice_id = voice_send['audio'][0]['file_id'] # это сам file_id
      res = cur.execute('UPDATE dictionary SET voice=%s WHERE id=%s;'% (voice_id,idd))
      con.commit()
  con.close()
