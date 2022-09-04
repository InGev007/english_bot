import random
import sqlite3
con = sqlite3.connect("bot.db")
cur = con.cursor()
res = con.execute('SELECT idd FROM tempdict WHERE idu=0 AND good<5 ORDER BY good')
res=res.fetchall()
con.commit()
coll=len(res)
#random.shuffle(res)
print(coll)