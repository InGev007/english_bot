import sqlite3
import random

def createuser(uid):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()
    res = con.execute('INSERT INTO users (id,chat) VALUES (%s,%s);'% (uid,0))
    con.commit()
    con.close()
    return

def checkstate(uid):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()
    res = con.execute('SELECT chat FROM users WHERE id=%s;'% uid)
    res=res.fetchone()
    con.commit()
    con.close()
    return res[0]

def setstate(uid,state):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()
    res = con.execute('UPDATE users SET chat=%s WHERE id=%s;'% (state,uid))
    res=res.fetchone()
    con.commit()
    con.close()

def startlearn(uid):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()
    res = con.execute('SELECT COUNT(idu) FROM tempdict WHERE idu=%s;'% uid)
    res=res.fetchone()
    con.commit()
    colln=res[0]+1
    i=0
    while i<50:
        res = con.execute('INSERT INTO tempdict (idu,idd) VALUES (%s,%s);'% (uid,colln+i))
        con.commit()
        i+=1
    i1=(random.randint(0, 1000),random.randint(0, 1000),random.randint(0, 1000))
    res = con.execute('SELECT ru FROM dictionary WHERE id in (%s,%s,%s)'% (i1[0],i1[1],i1[2]))
    res=res.fetchall()
    answ=[res[0][0],res[1][0],res[2][0]]
    res = con.execute('SELECT en,ru FROM dictionary WHERE id=%s;'% colln)
    res=res.fetchone()
    answ.append(res[1])
    sql = con.execute('INSERT INTO t_dial (idu,ganswer) VALUES (%s,"%s");'% (uid,answ[3]))
    con.commit()
    random.shuffle(answ)
    answ.append(res[0])
    con.close()
    return answ