from socket import *
import os
import signal
import pymysql
import time
import sys


DICT_TEXT='./dict.txt'
HOST='0.0.0.0'
PORT=8888
ADDR=(HOST,PORT)





def main():
    db = pymysql.connect(host="localhost",\
             user="root",password="123456",\
             database="project",charset="utf8")
    s=socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)
    #忽略子进程信号
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)
    print('listen the port 8888...')
    while True:
        try:
            c,addr=s.accept()
        except KeyboardInterrupt:
            sys.exit('服务器退出')
        except Exception as e:
            print('服务器异常:',e)
            continue
        print('已连接客户端',addr)
        pid= os.fork()
        if pid==0:
            s.close()
            do_child(c,db)
        else:
            c.close() 
            continue

def do_child(s,db):
    while True:
        data=s.recv(1024).decode()
        l=data.split(' ')
        if not data or data[0]=='E':
            s.close()
            sys.exit('客户端退出')
        if data[0]=='L':
            do_login(s,db,l[1],l[2])
        elif data[0]=='R':
            do_register(s,db,l[1],l[2])
        elif data[0]=='Q':
            do_query(s,db,l[1],l[2])
        elif data[0]=='H':
            do_hist(s,db,l[1])



def do_login(s,db,name,pd):
    cursor=db.cursor()
    sql_query="select * from user where name='%s'"%name
    cursor.execute(sql_query)
    data=cursor.fetchone()
    if data:
        if data[2]==pd:
            s.send(b'OK')
        else:
            s.send(b'FAIL')
    else:
        s.send(b'FAIL')



def do_register(s,db,name,passwd):
    cursor=db.cursor()
    sql_query="select * from user where name='%s'"%name
    cursor.execute(sql_query)
    if cursor.fetchone():
        s.send(b'EXITE')
        return
    try:
        sql="insert into user(name,password) values('%s','%s')"%(name,passwd)
        cursor.execute(sql)
        db.commit()
        s.send(b'OK')
    except:
        cursor.rollback()
        s.send(b'FAIL')

def do_query(c,db,name,word):
    cursor=db.cursor()

    def insert_history():
        tm=time.ctime()
        sql="insert into hist(name,word,time) values('%s','%s','%s')"%(name,word,tm)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    try:
        f=open(DICT_TEXT)
    except:
        c.send('查询失败'.encode())
        return
    for line in f:
        tmp=line.split(' ')[0]
        if tmp>word:
            c.send('查询失败'.encode())
            f.close()
            return
        elif tmp==word:
            insert_history()
            c.send(line.encode())
            f.close()
            return
    c.send('查询失败'.encode())
    f.close()

def do_hist(c,db,name):
    cursor=db.cursor()
    sql="select * from hist where name='%s'"%name
    cursor.execute(sql)
    r=cursor.fetchall()
    if not r:
        c.send('没有历史记录'.encode())
        time.sleep(0.1)
        c.send(b'##')
    for i in r:
        msg="%s  %s   %s"%(i[1],i[2],i[3])
        c.send(msg.encode())
        time.sleep(0.1)
    else:
        c.send(b'##')





if __name__=='__main__':
    main()