from socket import *
from getpass import getpass
import sys



def meun_one():
    print('**************')
    print('1)登录')
    print('2)注册')
    print('3)退出')
    print('**************')
def meun_two():
    print('**************')
    print('1)查询单词')
    print('2)查询历史记录')
    print('3)退出登录')
    print('**************')
        



def main():
    if len(sys.argv)<3:
        print('argv is error')
        return
    HOST=sys.argv[1]
    PORT=int(sys.argv[2])
    ADDR=(HOST,PORT)
    s=socket()
    try:
        s.connect(ADDR)
    except:
        sys.exit('连接服务器失败')
    while True:
        meun_one()
        cmd=input('请输入选项>>>')
        if cmd=='1':
            n=do_login(s)
            if n:
                print('登录成功')
                login(s,n)
            else:
                print('登录失败')
        elif cmd=='2':
            n=do_register(s)
            if n==0:
                print('注册成功')
            elif n==1:
                print('用户已经存在')
            elif n==2:
                print('注册失败')
        elif cmd=='3':
            s.send('E')
            sys.exit('客户端退出')
        else:
            print('输入错误请重新输入')
            sys.stdin.flush()

def do_login(s):
    while True:
        name=input('请输入姓名')
        pd=getpass('请输入密码')
        data='L '+name+' '+pd
        s.send(data.encode())
        data=s.recv(128).decode()
        if data=='OK':
            return name
        else:
            return 1

def do_register(s):
    while True:
        name=input('请输入姓名')
        pd=getpass('请输入密码')
        pd1=getpass('请再次输入密码')
        if (' ' in name) or (' ' in pd):
            print('用户名跟密码不许有空格')
            continue
        if pd != pd1:
            print('两次密码不一致')
            continue
        if not (name and pd):
            print('名字密码不能为空')
            continue

        data='R '+name+' '+pd
        s.send(data.encode())
        data=s.recv(128).decode()
        if data=='OK':
            return 0
        elif data=='EXITE':
            return 1
        else:
            return 2
def login(s,name):
    while True:
        meun_two()
        cmd=input('请输入选项')
        if cmd=='1':
            query(s,name)
        elif cmd=='2':
            history(s,name)
        elif cmd=='3':
            return
        else:
            print('输入错误请重新输入')
            sys.stdin.flush()
def query(s,name):
    while True:
        word=input('请输入查询单词:')
        if word=='##':
            break
        data='Q '+'name'+' '+word
        s.send(data.encode())
        print(s.recv(1024).decode())

def history(s,name):
    data='H '+'name'
    s.send(data.encode())
    while True:
        data=s.recv(1024).decode()
        if data=='##':
            break
        print(data)




if __name__=='__main__':
    main()
        