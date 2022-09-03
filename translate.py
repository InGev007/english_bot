import random
import sqlite3
import translators as ts

con = sqlite3.connect("bot.db")
cur = con.cursor()

res = con.execute('SELECT en FROM dictionary WHERE ru is Null')

#res = con.execute('SELECT en FROM dictionary')
res = res.fetchall()

for i in range(0, len(res)): 
    text=res[i][0]
    cell_obj = ts.google(text, to_language='ru')
    sql = con.execute('UPDATE dictionary SET ru="%s" WHERE en = "%s";'%(cell_obj,text))
    con.commit()
    print(i)
con.close()