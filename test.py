import random
import sqlite3
con = sqlite3.connect("bot.db")
cur = con.cursor()
res = con.execute('SELECT ru FROM dictionary WHERE id in (%s,%s,%s)'% (23,25,26))
res=res.fetchall()
con.commit()
answ=[res[0][0],res[1][0],res[2][0]]
answ.append('object')
print(answ)