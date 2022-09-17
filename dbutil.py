import sqlite3

import updatedb

def checkandupdatedb():
    con = sqlite3.connect("./db/bot.db")
    cur = con.cursor()
    res=con.executescript(updatedb.updatesql)
    con.commit()
    con.close()
    
def dumpdb():
    con = sqlite3.connect("./db/bot.db")
    with open('dump.sql', 'w', encoding='UTF8') as f:
        for line in con.iterdump():
            f.write('%s\n' % line)
    con.close()