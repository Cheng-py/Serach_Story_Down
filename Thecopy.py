import requests
from lxml import etree
import time
import os
import MySQLdb


class Story:
    def __init__(self):
        self.main_url = 'https://www.b520.cc/modules/article/search.php?'

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}

        self.db = MySQLdb.connect("localhost", "root", "123456", "spiders", charset='utf8')
        self.cursor = self.db.cursor()
        try:
            sql = """ 
            drop table bqg; 
            create table bqg(
            id int not null auto_increment primary key,
            title char(30),
            link varchar(50));
            truncate table bqg;
            """
            self.cursor.execute(sql)
            self.db.commit()
            # self.db.close()
        except:
            pass

    # 查看搜索到的页面。
    def serach(self):
        self.name = input("---------------可搜书名和作者,请您少字也别输错字。---------------" + "\n")
        self.url = self.main_url + "searchkey=" + str(self.name)
        rep = requests.get(url=self.url, headers=self.headers).text

        html = etree.HTML(rep)

        return html

    # 搜索到的小说名字与作者名和链接。
    def show(self):
        content = self.serach()
        book_link_dict = []
        number = 0
        book_list = content.xpath('//*[@id="hotcontent"]/table/tr[position()>1]/td[1]/a/text()')

        name_list = content.xpath('//*[@id="hotcontent"]/table/tr[position()>1]/td[@class="odd"][2]/text()')

        link_list = content.xpath('//*[@id="hotcontent"]/table/tr[position()>1]/td[1]/a/@href')
        if (len(book_list) == 0):
            print("查无此书.....")
            return self.show()

        for num in range(len(book_list)):

            number += 1
            book_link_dict.append({"id": number, "book": book_list[num], 'link': link_list[num]})

            if (number < 10):
                print("(0" + str(number) + ")" + ">>>" + book_list[num] + "-------" + name_list[num] + '\n', end='')
            else:
                print("(" + str(number) + ")" + ">>>" + book_list[num] + "-------" + name_list[num] + '\n', end='')
        return book_link_dict  # 返回整本书

    # 匹配用户想要的书
    def get(self):

        need = []
        book_link = self.show()
        ID = input("请输入需要的小说编号:" + '\n')

        try:
            ID = int(ID)
            if (ID):
                ID -= 1
                if not (ID > len(book_link) or ID < 0):  # 如果用户输入0的话，不处理就会成-1。会跳转到最后
                    book = book_link[int(ID)]['book']
                    link = book_link[int(ID)]['link']
                    need.append(book)
                    need.append(link)
                    return need
        except:
            print("不对，你再试试。")
            return self.get()  # 抛出异常，继续运行自己。

    def get_story_title_link(self):
        new_title_list = []  # 小说所有章节
        new_link_list = []  # 小说所有链接。
        all_dict = {"title": '', "link": " ", "book": ''}
        try:
            res = self.get()
            url = res[1]  # 书的链接。
            rep = requests.get(url=url, headers=self.headers).text
            html = etree.HTML(rep)

            title_xp = '//*[@id="list"]/dl/dd/a/text()'  # 获取具体页面的章节名与链接
            link_xp = '//*[@id="list"]/dl/dd/a/@href'

            title_list = html.xpath(title_xp)
            link_list = html.xpath(link_xp)
            for i in range(9, len(title_list)):  # 开始的几个为倒叙。
                if (title_list[i].startswith("第")):  # 以第开头。
                    new_title_list.append(title_list[i])
                    new_link_list.append(link_list[i])
                    all_dict['title'] = new_title_list  # 存到字典
                    all_dict['link'] = new_link_list

            all_dict['book'] = res[0]  # 把书名存进去
        except:
            pass
        return all_dict

    def save(self):  # 数据存到数据库。
        count = 0  # 计算多少条数据
        data = self.get_story_title_link()
        book = data['book']
        data.pop('book')
        titles = data['title']
        links = data['link']
        for num in range(len(titles)):
            sql = 'insert into bqg(title,link) values("' + str(titles[num]) + '","' + str(links[num]) + '");'
            self.cursor.execute(sql)
            count += 1
        self.db.commit()
        return count, book  # 返回有多少条数据

    def load(self, num):
        length, book = self.save()
        num = str(num)
        sql1 = "select title from bqg where id=" + num + ";"
        sql2 = "select link from bqg where id=" + num + ";"
        print(sql1)
        print(sql2)
        self.cursor.execute(sql1)
        title = self.cursor.fetchone()
        self.cursor.execute(sql2)
        link = self.cursor.fetchone()
        return str(title[0]), str(link[0]), length, book  # 返回字符串。将元组变为字符串。

    # 小说本说了
    def The_story(self):  # 获取小说所有章节与链接并下载

        num = 0  # 用来下载排序
        # title, link, length = self.load(num)
        title_link = self.get_story_title_link()  # 获取小说所有章节与链接。
        titles = title_link['title']  # list 类型
        links = title_link['link']
        book = title_link['book']  # 获取书名
        dict_link_title = (dict(zip(titles, links)))  # 将书名剔除，只留下章节名(key)，链接(value)
        dict_num = len(dict_link_title.keys())
        text_xp = '//*[@id="content"]/p/text()'
        for title, link in dict_link_title.items():
            try:
                num += 1  # 章节排序用

                req = requests.get(url=link, headers=self.headers, timeout=5)

                rep = req.text
                html = etree.HTML(rep)
                texts = html.xpath(text_xp)  # 一章节小说内容
                texts = str(texts)
                texts = texts.replace("\\u3000", '')  # 去掉\u3000
                texts = texts.replace("'", '')  # 去掉多余符号
                texts = texts.replace('\n', '')  # 替换成空格
                texts = texts[3:-1]  # 从第三个开始
                time.sleep(1)  # 一秒钟下载一章，给网站减少压力，也避免网速较差下载失败
                self.download(book, title, texts, num, length, link)
            except Exception as e:
                print("超时")

    def download(self, book, title, texts, num, dict_num, link):
        b = ''  # 用来接收一行输出50
        other_num = 0  # 用来表示剩余字数不够50字的文字下标。
        if not os.path.exists(os.getcwd() + "\\" + str(book)):
            os.makedirs(book)
        try:
            with open(os.getcwd() + "\\" + str(book) + "\\" + str(num) + str(title) + ".txt", "w",
                      encoding="utf-8") as fp:
                for text in texts:
                    b = b + text
                    if (len(b) % 50 == 0 and len(b) != 0):  # 每50个字换行一次，随自己调
                        other_num += 50
                        fp.write("\n" + b)
                        b = ''  # 初始化存储50个字符的容器。
                fp.write("\n" + texts[other_num:-1])  # 不够50字余下的文字。
                print(title + "         下载完成....." + "(" + str(num) + "/" + str(dict_num) + ")")  # 下载完成/总下载量
            fp.close()
        except:
            print("下载好像出错了........")


if __name__ == '__main__':
    st = Story()
    # st.The_story()
    # st.save()
    title, link, length, book = st.load(3)