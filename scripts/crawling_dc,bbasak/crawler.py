# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from bs4 import BeautifulSoup
from dcdao import DcDAO
from bbasakdao import BbasakDAO
import csv
import datetime
import re
import codecs
import threading
import time

def find_a(tags):
    return tags.name == 'a' and tags.has_attr('href') and tags.has_attr('class')

def find_table(tags):
    return tags.name == 'table' and not tags.has_attr('id') and tags.has_attr('class')

def find_a_not_class(tags):
    return tags.name == 'a' and not tags.has_attr('target')

# class DCinsidePostsCrawler(object):
#     def __init__(self, dcdao):
#         self.boarddao = dcdao
#
#
#     def get_page(self, pos, types):
#         no = 1
#         while True:
#             url = 'https://gall.dcinside.com/board/lists/?id=smartphone&page={}&search_pos={}&s_type=search_all&s_keyword={}'.format(no, pos, types)
#             data = requests.get(url)
#
#             content = data.content
#             soup = BeautifulSoup(content, 'html5lib')
#             table = soup.find('tbody', attrs={'class': 'list_tbody'})
#
#             group = table.find_all(find_a)
#             print(str(group[-1]['class'][0]))
#             if str(group[-1]['class'][0]) == 'icon_notice': # 페이지 범위 넘어가면 공지만 존재
#                 break
#
#             for a in group:
#                 link_text = str(a['class'][0])
#                 link = str(a['href'])
#                 if link_text != 'icon_notice': #운영자의 공지는 크롤링 제외
#                     self.crawl_everything(link,types)
#                 else:
#                     pass
#             no += 1
#
#
#     def crawl_everything(self, link, types):
#         url = 'https://gall.dcinside.com' + link
#         data = requests.get(url)
#         content = data.text
#
#         soup = BeautifulSoup(content, 'html5lib')
#
#         for script in soup(['script','style']):
#             script.extract()
#
#         title = soup.find('dd')
#         if title == None or title == '':
#             return
#         title = title.text
#         title = re.sub(',','',title)
#
#
#         contents = soup.find('div', attrs={'class':'s_write'})
#         if contents == None or contents == '':
#             return
#         content = contents.find('td')
#         content = " ".join(content.text.split())
#         content = re.sub(',','', content)
#
#         w_top_right = soup.find('div', attrs={'class':'w_top_right'})
#         date = w_top_right.find('b')
#         if date == None or date == ':':
#             return
#         date = date.text
#
#         w_top_left = soup.find('div', attrs={'class':'w_top_left'})
#         read = w_top_left.find_all('dd', attrs={'class':'dd_num'})[0]
#         read = read.text.strip()
#
#         try:
#             self.boarddao.save_posts(str(link), str(date), str(title), str(content), str(read), types)
#
#             # with codecs.open('dcinside_{}.csv'.format(types),'a','utf-8') as fa:
#             #     print(date)
#             #     #time.sleep(0.5)
#             #     writer = csv.writer(fa)
#             #     writer.writerow([str(link), str(date), title, str(content), datetime.datetime.now()])
#
#         except Exception, e:
#             print e


class BbasakPostsCrawler(object):
    def __init__(self, bbasakdao):
        self.bbasakdao = bbasakdao

    def get_page(self, type, start, end):
        no = 1
        while True:
            url = 'http://bbasak.com/bbs/board.php?bo_table=b001&sfl=wr_subject%7C%7Cwr_content&stx={}&sop=and&page={}'.format(type, no)
            data = requests.get(url)
            content = data.content
            soup = BeautifulSoup(content, 'html5lib')
            table = soup.find(find_table)

            if len(table.find_all('tr')) == 1:
                break

            for tr in table.find_all('tr'):
                td = tr.find('td', attrs={'class':'tit'})
                a = td.find('a')
                link = a['href']
                self.crawl_everything(link, type, start, end)

            no += 1

    def crawl_everything(self, link, type, start, end):
        res = requests.get(link)
        content = res.text

        soup = BeautifulSoup(content, 'html5lib')

        for script in soup(['script', 'style']):
            script.extract()

        view_title = soup.find('div', attrs={'class':'view_title_txt'})

        title = view_title.find('p', attrs={'class':'tit'})
        if title == None or title =='':
            return
        title = title.text.strip()
        title = re.sub(',', '', title)

        span = view_title.find_all('span', attrs={'class':'fwb'})
        date = span[1].text
        date = re.sub(r'(\d{2})-(\d{2})-(\d{2}) (\d{2}):(\d{2})', r'\1\2\3', date)

        # read = span[2].text
        # read = re.sub(',','',read)

        content = soup.find('div', attrs={'class','detailTxt'})
        content = " ".join(content.text.split())
        content = re.sub(',','',content)
        if (int(date) <= int(end)) & (int(date) >= int(start)):
            try:
                self.bbasakdao.save_posts(str(link), str(date), str(title), str(content), type)

                # with codecs.open('bbasak_{}.csv'.format(type),'a','utf-8') as fa:
                #     print(date)
                #     #time.sleep(0.5)
                #     writer = csv.writer(fa)
                #     writer.writerow([str(link), str(date), title, str(content), str(read), datetime.datetime.now()])
            except Exception, e:
                print e
        else:
            print(date, 'pass')
            pass


# dcdao = DcDAO()
# crawler = DCinsidePostsCrawler(dcdao)

# pos_g6 = -4470000
# while pos_g6 >= -4500000:
#     crawler.get_page(pos_g6,'g6')
#     pos_g6 -= 10000

# pos_g5 = -4340000
# while pos_g5 >= -4390000:
#     crawler.get_page(pos_g5, 'g5')
#     pos_g5 -= 10000
#
# pos_s7 = -4350000   #추가
# while pos_s7 >= -4390000:
#     crawler.get_page(pos_s7, 's7')
#     pos_s7 -= 10000
#
# pos_s6 = -4210000    #4개 추가로
# while pos_s6 >= -4300000:
#     crawler.get_page(pos_s6, 's6')
#     pos_s6 -= 10000

bbasakdao = BbasakDAO()
crawler = BbasakPostsCrawler(bbasakdao)
crawler.get_page('g6', '161010', '170403')
