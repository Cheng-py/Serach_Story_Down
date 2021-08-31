# test1 =['ha','ha']
#
# a = [{"b":}]
# print(a)

# a = 'asdad'
# print((a).isnumeric())
#
# def test():
#     a = 'aaa'
#     b = 'b'
#     return a,b

# res = test()[0]
# print(res)
# a = []
# for i in range(10):
#     b = {'a':i}
#     a.append(b)
#
# print(type(len(a)))
# ID = input("请输入需要的小说编号" + '\n')

# try:
#     ID = int(ID)
#     if (ID):
#         ID -= 1
#     else:
#         print("Errot")
#
# except:
#     print("error")
#
# a = 1
# b = 2
# c = []
# c.append(a)
# c.append(b)
# print(c)


from lxml import etree
import requests
import re
# url = 'http://www.b520.cc/0_105/'
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}

# xp = '//*[@id="list"]/dl/dd/a/text()'
# xp2 = '//*[@id="list"]/dl/dd/a/@href'
# res = requests.get(url=url,headers=headers).text
# html = etree.HTML(res)
# itle_Re = r"[\u7b2c](.|\n)*[\u7ae0]"
# ss = html.xpath(xp)
# link = html.xpath(xp2)
# for i in range(9,len(ss)):
#     if(ss[i].startswith("第")):
#         print(ss[i]+link[i])
#     # print(ss[i])
#
# a = {"t":''}
# b= []
# for i in range(1,5):
#     b.append(i)
#     a['t'] =b
# print(a)
#
# for i in range(9,11):
#     print(i)

# xp = '//*[@id="content"]/p/text()'
# url = 'http://www.b520.cc/0_105/179462351.html'
# rep = requests.get(url=url,headers=headers).text
# html = etree.HTML(rep)
#
# la = html.xpath(xp)
# for i in range(len(la)-1):
#     print(la[i])


# g = {'a':13,'b':2}
# for key,value in g.items():
#     print(key)
import re
# a = "['\u3000\u3000;', '\u3000\u3000他从迷迷糊糊中醒过来]"
# a.replace(u'\u3000',u' ')
# print(a)


# a = ['他从迷迷糊糊中醒过来，看见的是白色的蚊帐，头上隐隐作痛，不知道这是在怎样的环境里，于是闭上眼睛想了很久，才微微叹了口气。, 没有死。, 那么，自己现在是在被软禁着？, 掀开被子坐起来，大约是昏迷了很久，与身体之间还无法很好的协调，低头看看，衣服的样式怪里怪气的，布料也很差，直到站起在房间的地板上，才发现更多无法协调的东西。, 老式的房屋、老式的床、桌椅板凳，虽然用料和做工都不错，但整个房间都是仿古的摆设，也有看起来很棒的瓷器，但任何现代化的电子设备都不存在了。你搞什么，唐明远？想起那戴眼镜的家伙，心中暗骂了一句，随后……, 这只手也变了，自己的手……不像是自己的。, 他看了看两只显得苍白的手，片刻，才在桌椅前坐下，解开身上的衣服，这具身体……没有弹孔。开什么玩笑？自己明明记得那么多子弹对着自己射过来的，前前后后都有啊，难不成是做了整形手术？不对，这具身体都不是自己的，所有的特征都在表现出这个迹象，']

# a={"a":1,"b":2}
# print(len(a.keys()))

# from func_timeout import func_set_timeout
# import func_timeout
# import time
# @func_set_timeout(3)
# def test(num):
#     num-=1
#     time.sleep(num)
#     print("time")
#     return test

# try:
#     test(5)
# except:
#     print("超时")
#     test(5)
# a = {'a':"",'b':""}
# def test():
#     for i in range(1,11):
#         a['a']=i
#         a['b'] = i+10
#     return a


# for i in test():
# #     print(i)
# print(test())

# from threading import Thread
#
# def a(num):
#     for i in range(10):
#         print("我是a"+str(i+num))
#
# def b():
#     for i in range(10):
#         print("我是b"+str(i+3))
#
# t1 = Thread(target=a)
# t2 = Thread(target=b)
# t2.run()
# t1.run()

# a = "12312312313adasdasdasadsdasdadadadasdsadasasdasdasdadsadaddasdsa2"*33
# b=''
# num = 0
# for i in a:
#     b=b+i
#     if(len(b)%50==0):
#         num+=50
#         print(b)
#         print("换行")
#         b=''
# print(a[num:-1])
#     print(a[num])
# print(len(a))
# print(a[:50])


# import urllib
# from urllib import request
# # 案例1
# import urllib.request
# url="http://www.b520.cc/0_105/71563.html"
# #注意：在urllib 中这种的headers 是需要是字典的
# headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE"}
# req=urllib.request.Request(url=url,headers=headers)
# file=urllib.request.urlopen(req)
#
# #出现有些解码错误的话，加上“ignore”就可以啦
# print(file.read().decode("utf-8",'ignore'))
#
# import requests
# rr = requests.get(url,headers=headers)
# print(rr.text)

#方法一 直接调用import time
import time
import random
from multiprocessing import Process
def run(name):
    print('%s runing' %name)
    # time.sleep(random.randrange(1,5))
    # print('%s running end' %name)


# if __name__ == '__main__':
#
#     p1=Process(target=run,args=('anne',)) #必须加,号
    # p2=Process(target=run,args=('alice',))
    # p3=Process(target=run,args=('biantai',))
    # p4=Process(target=run,args=('haha',))
    #
    # p1.start()
    # p2.start()
    # p3.start()
    # p4.start()
    # print('主线程')


# a = {"a":1,'b':2}
# # a.pop("a")
# print(len(a))
# print(len(a.keys()))
#
# key = 'asdad'
# value = ' asdasd'
# print('values('+key+','+value+')')
# a = '121323'
# print(a+'""')

# a = 1
# c = 'qweqe'
# print(c+str(a))
# num=1
# num =str(num)
# print("select link from bqg where id="+num+";")
# def test():
#     a=10
#     b=20
#     return a,b
# x,a = test()
# print(x)

# num =0
#
# while True:
#     num += 1
#     if num >10:
#         break
#     print(num)

# try:
#     i ='qada'
#     a=10
#     a=a+i
#     print("正常")
# except:
#     print("不正常")
#     print(a)

# def test(num):
#     if(num>1):
#         return True
#     else:
#         return False
#
# if  not(test(0)):
#     print("dui")
# else:
#     print("cuo")

# a = True
# num = 0
# while a:
#     num+=1
#     if(num>10):
#         # a=False
#         break
#     print(num)
import MySQLdb
import pinyin

# def tn():
#     str1 = input("")
#     sr=''
#     for i in str(str1):
#         sr+=pinyin.get([i])[0]
#     print(sr)
# # tn()
# # print(pinyin.get("程")[0])
# db = MySQLdb.connect("localhost","root","123456","spiders",charset = 'utf8')
# cursor = db.cursor()
#
# sql = "select count(*) from zx;"
# res = cursor.execute(sql)
# print(res)
# test1 = 'test1'
# sql2 = "select * from {}".format(test1)
# try:
#     if cursor.execute(sql2):
#         print('y')
#     else:
#         print('false')
# except: # 报错就是表不存在。
#     sql = """
#                 create table {}(
#                 id int not null auto_increment primary key,
#                 title char(30),
#                 link varchar(50));""".format(test1)
#     cursor.execute(sql)
#     db.commit()
# cursor.execute(sql2)
# db.commit()

# def add():
#     sql = 'insert into test1(title,link) values("a","b")'
#     cursor.execute(sql)
#     db.commit()
#
# def delete(num):
#     sql = "delete from test1 where id="+str(num)+""
#     cursor.execute(sql)
#     db.commit()
#
# for i in range(42):
#     delete(i)
# def search():
#     sql = "select * from test1"
#     if(cursor.execute(sql)):
#         print("True")
#     else:
#         print("False")
# # delete(3)
# search()
# db.close()

# x = ''
# def func(a, b, c):
#     global x  # <- here
#     if a == b:
#         x = "bqg"
#     elif b == c:
#         x = 'zx'
# func(1,1,1)
# print("我是x"+x)
# a = """ asdad
#
# dada%s(name)
# dasda
# asdad{}""".format(123,12323)
# print(a)

# class T1:
#
#     def __init__(self):
#         self.get()
#
#     def get(self):
#         global x
#         x=''
#         x+="bqg"
#         # print(x)
#
#
#     def load(self):
#         self.get()
#         print(x)
#
#     def lal(self):
#         print(x)
# t = T1()
# # t.get()
# t.load()
# t.lal()
# # print(t.x)
#
# tableName="bqg"
# sql2 = """
#                 truncate table {};
#                 drop table {}
#                 create table {}(
#                 id int not null auto_increment primary key,
#                 title char(30),
#                 link varchar(50));
#                 """.format(tableName,tableName,tableName)
#
# print(sql2)

# tableName = 'asda'
# sql2 = """
#                 truncate table {};
#                 drop table {};
#                 create table {}(
#                 id int not null auto_increment primary key,
#                 title char(30),
#                 link varchar(50));
#                 """.format(tableName,tableName,tableName)
#
# print(sql2)
# y = 'y'
# class T:
#     def __init__(self):
#         pass
#
#     def gb(self,x):
#         global y
#         y+=str(x)
#
#     def ct(self):
#         self.gb(123)




#     def t2(self):
#         # global y
#         print(y)
# print(y)
# t = T()
# t.gb(123)
# t.t2()

# def test1(x,y):
#     if(x>y):
#         print("存在")
#         return True
#     else:
#         print("创建")
#         return False
#
# if (test1(1,2)):
#     print("小于")
# else:
#     print("大于")


import MySQLdb
db = MySQLdb.connect("localhost","root","123456","spiders",charset = 'utf8')
cursor = db.cursor()
tableName = 'zx'
sql = "select title from zx where id=10"  # 计算多少条数据
sql2 = "select link from zx"  # 计算多少条数据
s3 = "select id from zx;"


cursor.execute(s3)
rs = cursor.fetchone()

print(str(rs[0]))

cursor.execute(sql)
res = cursor.fetchone()
cursor.execute(sql2)

res2 = cursor.fetchone()
res = str(res[0])
print(res)
print(res2)
print(type(res))




