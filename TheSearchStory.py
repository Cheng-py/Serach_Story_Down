import requests
from lxml import etree
import time
import os
import MySQLdb  # 数据库
import pinyin   # 获取首字母
import shutil  # 删文件

tableName = ''  # 数据库表名通过小说首字母缩写
class Story:
    def __init__(self):
        self.main_url = 'https://www.b520.cc/modules/article/search.php?'
        self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}
        self.db = MySQLdb.connect("localhost","root","123456","spiders",charset = 'utf8') # 连接数据库
        self.cursor = self.db.cursor()  # 创建游标

    def return_Tablename(self,bookname):  # 单纯获取书名。取首字母建表。
        global tableName
        for i in str(bookname):
            tableName+=pinyin.get([i])[0]
        return tableName

    def createTable(self):
        try:   # 报错就代表表不存在。
            sq1 = "select count(*) from "+str(tableName)
            res = self.cursor.execute(sq1)

            if(int(res)>=0):  # 判断数据库有没有数据，否则创建
                print("继续上次下载...........")
                return True

        except:  # 删表报错就创建。
            sql2 = """
                            create table {}(
                            id int not null auto_increment primary key,
                            title char(30),
                            link varchar(50));      
                            """.format(tableName)
            self.cursor.execute(sql2)
            self.db.commit()
            print("开始下载............")
            return False


# 查看搜索到的页面。
    def serach(self):
        self.name = input("---------------可搜书名和作者,请您少字也别输错字。---------------" + "\n")
        self.url = self.main_url + "searchkey=" + str(self.name)
        rep = requests.get(url = self.url ,headers = self.headers).text

        html = etree.HTML(rep)

        return html

# 搜索到的小说名字与作者名和链接。
    def show(self):
        content = self.serach()
        book_link_dict = []
        number = 0
        book_list = content.xpath('//*[@id="hotcontent"]/table/tr[position()>1]/td[1]/a/text()')

        name_list = content.xpath('//*[@id="hotcontent"]/table/tr[position()>1]/td[@class="odd"][2]/text()')

        link_list =content.xpath('//*[@id="hotcontent"]/table/tr[position()>1]/td[1]/a/@href')
        if (len(book_list) == 0):
            print("查无此书.....")
            return self.show()

        for num in range(len(book_list)):

            number += 1
            book_link_dict.append({"id":number,"book":book_list[num],'link':link_list[num]})

            if(number<10):
                print("(0"+str(number)+")"+">>>"+book_list[num]+"-------"+name_list[num]+'\n',end='')
            else:
                print("(" + str(number) + ")" + ">>>" + book_list[num] + "-------" + name_list[num] + '\n',end='')
        return book_link_dict # 返回整本书

# 匹配用户想要的书
    def get(self):

        need = []
        book_link = self.show()
        ID = input("请输入需要的小说编号:"+'\n')
        try:
            ID = int(ID)
            if(ID):
                ID-=1
                if not (ID > len(book_link) or ID < 0): # 如果用户输入0的话，不处理就会成-1。会跳转到最后
                    book = book_link[int(ID)]['book']
                    link = book_link[int(ID)]['link']
                    need.append(book)
                    need.append(link)
                    return need
        except:
            print("不对，你再试试。")
            return self.get() # 抛出异常，继续运行自己。



    def get_story_title_link(self):
        new_title_list = []  # 小说所有章节
        new_link_list = []  # 小说所有链接。
        all_dict = {"title":'',"link":" ","book":''}
        try:
            res = self.get()
            url = res[1]  # 书的链接。
            rep = requests.get(url=url,headers = self.headers).text
            html = etree.HTML(rep)

            title_xp = '//*[@id="list"]/dl/dd/a/text()'  # 获取具体页面的章节名与链接
            link_xp = '//*[@id="list"]/dl/dd/a/@href'

            title_list = html.xpath(title_xp)
            link_list = html.xpath(link_xp)
            for i in range(9,len(title_list)): # 开始的几个为倒叙。
                if (title_list[i].startswith("第")):  # 以第开头。
                    new_title_list.append(title_list[i])
                    new_link_list.append(link_list[i])
                    all_dict['title'] = new_title_list   # 存到字典
                    all_dict['link'] = new_link_list

            all_dict['book'] = res[0] # 把书名存进去
        except:
            pass
        return all_dict

    def save(self):  # 数据存到数据库。
        # 有tableName
        try:
            data = self.get_story_title_link()
            book = data['book']
            book = str(book)
            data.pop('book')
            if(tableName==''):
                self.return_Tablename(book)
            else:
                pass
            titles = data['title']
            links = data['link']
            count = len(links)
            if not (self.createTable()):  # 没表就创建表以及插入数据。
                for num in range(len(titles)):
                    sql = 'insert into '+tableName+'(title,link) values("'+str(titles[num])+'","'+str(links[num])+'");'
                    self.cursor.execute(sql)
                self.db.commit()

                return count,book  # 小说章节总数。
            else:  # 数据库有数据。
                return count,book  #  小说剩余章节的总数。
        except:
            print("save失败\n")

    def load(self,num):
        num = str(num)
        try:
            sql1 = "select title from "+tableName+" where id="+num+";"
            sql2 = "select link from "+tableName+" where id="+num+";"
            self.cursor.execute(sql1)
            title = self.cursor.fetchone()
            title = str(title[0])

            self.cursor.execute(sql2)
            link=self.cursor.fetchone()
            link = str(link[0])

            return title,link  # 返回字符串。将元组变为字符串。
        except:
            print("load报错了\n")

    def delete(self,num):
        num = str(num)
        sql = "delete from "+tableName+" where id="+num+";"
        self.cursor.execute(sql)
        self.db.commit()

    def get_book_id(self,strs):   # 用来查看文件名前面的数字
        while True:
            if (strs[:5].isnumeric()):
                return int(strs[:5])

            elif (strs[:4].isnumeric()):
                return int(strs[:4])

            elif (strs[:3].isnumeric()):
                return int(strs[:3])

            elif (strs[:2].isnumeric()):
                return int(strs[:2])

            elif (strs[:1].isnumeric()):
                return int(strs[:1])

    def get_path(self,path):
        return os.getcwd()+"\\"+path

    def get_next_file(self,path):
        for i,j,k in os.walk(path):
            return k[-1]

    def get_dir_len(self,path):
        return len(os.listdir(path))

    # 小说本说了
    def The_story(self):  # 获取小说所有章节与链接并下载

          # 用来下载排序
        flag = True
        length,book = self.save()  # 获取有多少条数据和书名。
        sql_id = "select id from "+tableName
        self.cursor.execute(sql_id)
        id = self.cursor.fetchone()
        id =id[0]-1         # 获取当前数据库的ID，用来断点下载。
        Test_id = id  # 数据库的ID
        path = self.get_path(book)

        try:                            # 判断文件是不是少了或者误删了一部分。
            if not os.path.exists(path):
                os.mkdir(path)
            else:
                dir_len = self.get_dir_len(path)
                if(dir_len<Test_id):
                    YN = input("文件丢失，是否重新下载: 是 (Y) 否 (N)")
                    if(YN=='y' or YN =='Y'):
                        self.drop(tableName)
                        print(tableName)
                        shutil.rmtree(path) # 删掉整个某小说目录。
                        print("重新下载............")
                        self.The_story()
                    elif(YN == 'N' or YN =="n"):
                        pass
                    else:
                        print("输入错误")
                        return 0
        except:
            print("重下载有误")

        text_xp = '//*[@id="content"]/p/text()'  # 小说内容的xpath

        while flag:

            n = 0 # 控制下载超时重复循环下载
            id += 1  # 章节排序用

            if id > length:  # 循环到最后
                print("############################### 下载完成！###############################")
                # 判断下载完。下载完成后清除数据库。
                self.drop(tableName)
                self.cursor.close()
                self.db.close()

                return 0

            title,link = self.load(id)  # 都是 str

            try:
                req = requests.get(url=link, headers=self.headers, timeout=5)
                rep = req.text
                html = etree.HTML(rep)
                texts = html.xpath(text_xp)  # 一章节小说内容
                texts = str(texts)
                texts = texts.replace("\\u3000", '')  # 去掉\u3000
                texts = texts.replace("'", '')  # 去掉多余符号
                texts = texts.replace('\n', '')  # 替换成空格
                texts = texts[3:-1]  # 从第三个开始

                if(self.download(book, title, texts, id, length)):# 一秒钟下载一章，给网站减少压力，也避免网速较差下载失败
                    time.sleep(1)

            except:
                print("当前网络较差,正在重试..........")
                while(n<5):  # 超时重复下载。直到下载成功。
                    self.download(book, title, texts, id, length)  # 多重试下载。
                    if not(self.download(book, title, texts, id, length)):

                        break
                    n += 1
                    time.sleep(1)

    def download(self,book,title,texts,num,dict_num):

        b = ''  # 用来接收一行输出50
        other_num = 0  # 用来表示剩余字数不够50字的文字下标。
        if not os.path.exists(os.getcwd() + "\\" + str(book)):  # 小说不在就创建小说目录
            os.makedirs(book)
        try:
            if os.path.exists(os.getcwd() + "\\" + str(book) + "\\" + str(num) + str(title)+".txt"):  # 新建小说不存在才下载
                return False
            else:
                with open(os.getcwd() + "\\" + str(book) + "\\" + str(num) + str(title) + ".txt", "w",encoding="utf-8") as fp: # 当前目录的主目录下
                    for text in texts:
                        b = b+text
                        if(len(b)%50==0 and len(b)!=0): # 每50个字换行一次，随自己调
                            other_num+=50
                            fp.write("\n" + b)
                            b=''  # 初始化存储50个字符的容器。
                    fp.write("\n" + texts[other_num:-1])  # 不够50字余下的文字。

                    print(title + "         下载完成....." + "(" + str(num) + "/" + str(dict_num) + ")")   # 下载完成/总下载量

                    fp.close()

                    self.delete(str(num))

                return True
        except:
            print("下载好像出错了........")

    def drop(self,name):

        sql = "truncate table %s" %str(name)
        sql2 = "drop table %s"  %str(name)
        self.cursor.execute(sql)
        self.cursor.execute(sql2)




if __name__ == '__main__':
    st = Story()
    st.The_story()
    # st.drop('zx')
    # st.drop('zxzx')
    # 六脉文圣
