import sqlite3
import random

def createuser(uid):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()
    try:
        res = con.execute('INSERT INTO users (id,chat) VALUES (%s,%s);'% (uid,0))
    except:
        res = con.execute('UPDATE users SET chat=0 WHERE id=%s;'% uid)
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

def randansw():
    con = sqlite3.connect("bot.db")
    cur = con.cursor()
    i1=list(range(1, 1000))
    random.shuffle(i1)
    res = con.execute('SELECT ru FROM dictionary WHERE id in (%s,%s,%s)'% (i1[0],i1[1],i1[2]))
    res=res.fetchall()
    answ=[res[0][0],res[1][0],res[2][0]]
    con.close()
    return answ

def startlearn(uid):
    con = sqlite3.connect("bot.db")
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
    res = con.execute('SELECT en,ru,id FROM dictionary WHERE id IN (SELECT idd FROM tempdict WHERE idu=%s);'% uid)
    res=res.fetchall()
    random.shuffle(res)
    answ.append(res[0][1])
    sql = con.execute('INSERT INTO t_dial (idu,ganswer,idd) VALUES (%s,"%s",%s);'% (uid,answ[3],res[0][2]))
    con.commit()
    random.shuffle(answ)
    answ.append(res[0][0])
    con.close()
    return answ

def nextlearn(uid, text):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()
    res = con.execute('SELECT ganswer,idd FROM t_dial WHERE idu=%s;'% uid)
    res=res.fetchone()
    answ=res
    res = con.execute('DELETE FROM t_dial WHERE idu=%s;'% uid)
    con.commit()
    idd=answ[1]
    if answ[0]==text:
        res = con.execute('UPDATE tempdict SET good=good+1, wrong=0, ok= CASE WHEN (ok=0 AND good = 4) OR (ok=1) THEN 1 ELSE 0 END WHERE idd=%s AND idu=%s;'% (idd,uid))
        ret="Правильный ответ. Следующие слово: "
    else:
        res = con.execute('UPDATE tempdict SET good=0,wrong=1 WHERE idd=%s AND idu=%s;'% (idd,uid))
        ret = "Неправильно. Правильный ответ: " + answ + ". Следующие слово: "
    con.commit()
    res = con.execute('SELECT idd FROM tempdict WHERE idu=%s AND ((good<5 AND ok=0)OR(good<2 AND ok=1)) ORDER BY good;'%uid)
    res=res.fetchall()
    tempdict=res
    coll=len(tempdict)
    if coll==0:
        setstate(uid,0)
        res = con.execute('UPDATE tempdict SET good=0, wrong=0, ok=1 WHERE idu=%s'%uid)
        ret = "Ты успешно выучил ещё 50 слов. Продолжай в том-же духе и помни перерыв в обучении сведёт весь успех к нулю."
        con.commit()
        con.close()
        return ret,0
    else:
        random.shuffle(tempdict)
        res = con.execute('SELECT en,ru,id FROM dictionary WHERE id=%s;'% tempdict[0][0])
        res=res.fetchone()
        answ=randansw()
        answ.append(res[1])
        sql = con.execute('INSERT INTO t_dial (idu,ganswer,idd) VALUES (%s,"%s",%s);'% (uid,answ[3],res[2]))
        con.commit()
        random.shuffle(answ)
        con.close()
        ret=ret+res[0]
        return ret, answ

def undolearn(uid):
    con = sqlite3.connect("bot.db")
    cur = con.cursor()
    res = con.execute('DELETE FROM t_dial WHERE idu=%s;'% uid)
    res = con.execute('DELETE FROM tempdict WHERE idu=%s AND ok=0;'% uid)
    con.commit()
    res = con.execute('UPDATE tempdict SET good=0, wrong=0 WHERE idu=%s'%uid)
    con.commit()
    con.close()
    return