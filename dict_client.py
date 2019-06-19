"""
 dict 客户端
 功能： 根据用户输入,发送请求,得到结果
 结构： 一级界面  ----> 注册 登录 退出
       二级界面 -----> 查单词 历史记录 注销

"""

from socket import *
from getpass import getpass #运行使用终端
import sys,time


#服务器地址
ADDR='176.234.10.34',8888

#功能函数都需要套接字,定义为全局变量
s = socket()
s.connect(ADDR)

#注册函数
def do_register():
    while True:
        name=input("User:")
        passwd=getpass()
        passwd_=getpass("Again:")

        if (' ' in name) or (' ' in passwd):
            print("用户或密码不能有空格")
            continue
        if passwd != passwd_:
            print("两次密码不一致")
            continue

        msg='R %s %s'%(name,passwd)
        #发送请求
        s.send(msg.encode())
        #接收反馈信息
        data=s.recv(128).decode()
        if data=='OK':
            print("注册成功")
            time.sleep(3)
            #进入二级界面
            login(name)
        else:
            print("注册失败")
        return

#登录函数
def do_login():
    name=input("用户名：")
    passwd=getpass("密码：")
    msg="L %s %s"%(name,passwd)
    #发送请求
    s.send(msg.encode())
    #接收反馈信息
    data=s.recv(128).decode()
    if data=="OK":
        print("您已成功登录")
        #进入二级界面
        login(name)
    else:
        print("用户名或密码不正确")


#搭建网络
def main():
    #一级界面
    while True:
        print("""
        =============Welcome===============
        1.注册         2.登录        3.退出
        ===================================
        """)
        cmd=input("选择")
        if cmd=='1':
            do_register()
        elif cmd=='2':
            do_login()
        elif cmd=='3':
            s.send(b'E')
            sys.exit("谢谢使用")
        else:
            print("请输入正确选项")


#查单词
def do_query(name):
    while True:
        word=input("请输入单词：")
        #结束单词查询
        if word=="##":
            break
        msg="Q %s %s"%(name,word)
        #发送请求
        s.send(msg.encode())
        #接收请求
        data=s.recv(2048).decode()
        print(data)

#查询历史记录
def do_hist(name):
    msg="H %s"%name
    s.send(msg.encode())
    data=s.recv(128).decode()
    if data=="OK":
        while True:
            data=s.recv(1024).decode()
            if data=="##":
                break
            print(data)
    else:
        print("没有历史记录")
def login(name):
    #二级界面
    while True:
        print("""
        =============Welcome===============
        1.查单词     2.历史记录      3.注销
        ===================================
        """)
        cmd=input("选择")
        if cmd=='1':
            do_query(name)
        elif cmd=='2':
            do_hist(name)
        elif cmd=='3':
            return
        else:
            print("请输入正确选项")

if __name__=="__main__":
    main()