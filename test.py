import random
import sqlite3
con = sqlite3.connect("bot.db")
cur = con.cursor()
res = con.execute('SELECT id FROM dictionary WHERE id NOT IN (SELECT idd FROM tempdict WHERE idu=786607486);')
res=res.fetchall()
con.commit()
random.shuffle(res)
print(res[0][0])
con.close()