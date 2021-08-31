import requests
from lxml import etree
import time
import os
import MySQLdb
import pinyin


tableName = ''
class Story:
    def __init__(self):
        self.main_url = 'https://www.b520.cc/modules/article/search.php?'
        self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}
        self.db = MySQLdb.connect("localhost","root","123456","spiders",charset = 'utf8')
        self.cursor = self.db.cursor()

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
                print("继续上次下载........")
                return True
            else:
                pass
        except:  # 删表报错就创建。
            sql2 = """
                            create table {}(
                            id int not null auto_increment primary key,
                            title char(30),
                            link varchar(50));      
                            """.format(tableName)
            self.cursor.execute(sql2)
            self.db.commit()
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
        data = self.get_story_title_link()
        book = data['book']
        book = str(book)
        data.pop('book')
        self.return_Tablename(book)
        titles = data['title']
        links = data['link']
        sql_sum2 = "select id from " + tableName + ";"  # 计算多少条数据
        if not (self.createTable()):
            for num in range(len(titles)):
                sql = 'insert into '+tableName+'(title,link) values("'+str(titles[num])+'","'+str(links[num])+'");'
                self.cursor.execute(sql)
            self.db.commit()

            self.cursor.execute(sql_sum2)
            count2 = self.cursor.fetchall()
            count2 = len(count2)
            return count2,book
        else:
            print("不重复了")
            print(sql_sum2)
            self.cursor.execute(sql_sum2)
            count2 = self.cursor.fetchall()
            count2 = len(count2)
            return count2,book

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
            print("我在load里")
            print(title,link)
            return title,link  # 返回字符串。将元组变为字符串。
        except:
            print("load报错了")

    def delete(self,num):
        num = str(num)
        sql = "delete from "+tableName+" where id="+num+";"
        self.cursor.execute(sql)
        self.db.commit()

# 小说本说了
    def The_story(self):  # 获取小说所有章节与链接并下载

          # 用来下载排序
        flag = True
        length,book = self.save()  # 获取有多少条数据和书名。
        num = 0
        # id_sql = "select id from" + tableName
        # self.cursor.execute(id_sql)
        # num = self.cursor.fetchone()
        #
        # num = str(num[0])
        # print(num)

        book = str(book)
        text_xp = '//*[@id="content"]/p/text()'  # 小说内容的xpath
        print("走到了Flag")
        while flag:
            print("在flag里面")
            n = 0
            num += 1  # 章节排序用
            print("我在load上面")
            title,link = self.load(num)  # 都是 str
            print("我在load下面")
            print("我是wile里面的"+title)

            if num > length:  # 循环到最后
                print("ImStop")
                break
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

                if(self.download(book, title, texts, num, length)):# 一秒钟下载一章，给网站减少压力，也避免网速较差下载失败
                    time.sleep(1)
                    print("我在暂停")
            except:
                print("当前网络较差,正在重试..........")
                while(n<5):  # 超时重复下载。直到下载成功。
                    self.download(book, title, texts, num, length)  # 多重试下载。
                    if not(self.download(book, title, texts, num, length)):

                        break
                    n += 1
                    time.sleep(1)

    def download(self,book,title,texts,num,dict_num):
        print("调用下载了")
        b = ''  # 用来接收一行输出50
        other_num = 0  # 用来表示剩余字数不够50字的文字下标。
        if not os.path.exists(os.getcwd() + "\\" + str(book)):
            os.makedirs(book)
        try:
            if os.path.exists(os.getcwd() + "\\" + str(book) + "\\" + str(num) + str(title)+".txt"):  # 新建小说不存在才下载
                return False
            else:
                with open(os.getcwd() + "\\" + str(book) + "\\" + str(num) + str(title) + ".txt", "w",encoding="utf-8") as fp:
                    for text in texts:
                        b = b+text
                        if(len(b)%50==0 and len(b)!=0): # 每50个字换行一次，随自己调
                            other_num+=50
                            fp.write("\n" + b)
                            b=''  # 初始化存储50个字符的容器。
                    fp.write("\n" + texts[other_num:-1])  # 不够50字余下的文字。

                    print(title + "         下载完成....." + "(" + str(num) + "/" + str(dict_num) + ")")   # 下载完成/总下载量

                    fp.close()
                    print("我关闭了")
                    self.delete(str(num))
                    print("我删除了")
                return True
        except:
            print("下载好像出错了........")

if __name__ == '__main__':
    st = Story()
    st.The_story()
    st.db.close()