import sqlite3
from gtts import gTTS
import os
from aiogram.types import FSInputFile

def checkandupdatevoice():
  con = sqlite3.connect("./db/bot.db")
  cur = con.cursor()
  res = cur.execute('SELECT id, en FROM dictionary WHERE voice is NULL')
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
      voice_id = FSInputFile("./speech/%s.mp3"%(id,mytext.replace("'", "")))
      res = cur.execute('UPDATE dictionary SET voice=%s WHERE id=%s;'% (voice_id,idd))
      con.commit()
  con.close()
