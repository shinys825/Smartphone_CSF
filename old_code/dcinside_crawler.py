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

def find_a(tags):
    return tags.name == 'a' and tags.has_attr('href') and tags.has_attr('class')

def find_table(tags):
    return tags.name == 'table' and not tags.has_attr('id') and tags.has_attr('class')

def find_a_not_class(tags):
    return tags.name == 'a' and not tags.has_attr('target')

class DCinsidePostsCrawler(object):
    def __init__(self, dcdao):
        self.boarddao = dcdao


    def get_page(self, pos, types):
        url = 'http://gall.dcinside.com/board/lists/?id=smartphone&page={}&search_pos={}&s_type=search_all&s_keyword={}'
        no = 1
        while True:
            url = url.format(no, pos, types)
            hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
            try:
                data = requests.get(url, headers=hdr)
            except requests.exceptions.ConnectionError:
                return
            content = data.content
            soup = BeautifulSoup(content, 'html5lib')
            table = soup.find('tbody', attrs={'class': 'list_tbody'})

            group = table.find_all(find_a)

            if group[-1].find('td',attrs={'class':'t_hits'}) == '': # 페이지 범위 넘어가면 공지만 존재
                break

            for a in group:
                link_text = a['class']
                link = a['href']
                if link_text != 'icon_notice': #운영자의 공지는 크롤링 제외
                    self.crawl_everything(link)
                else:
                    pass
            no += 1


    def crawl_everything(self, link):
        url = 'http://gall.dcinside.com' + link
        hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
        try:
            data = requests.get(url, headers=hdr)
        except requests.exceptions.ConnectionError:
            print('e')

        content = data.text

        soup = BeautifulSoup(content, 'html5lib')

        for script in soup(['script','style']):
            script.extract()

        title = soup.find('dd')
        if title == None or title == '':
            return
        title = title.text
        title = re.sub(',','',title)


        contents = soup.find('div', attrs={'class':'s_write'})
        if contents == None or contents == '':
            return
        content = contents.find('td')
        content = " ".join(content.text.split())
        content = re.sub(',','', content)

        w_top_right = soup.find('div', attrs={'class':'w_top_right'})
        date = w_top_right.find('b')
        if date == None or date == ':':
            return
        date = date.text

        w_top_left = soup.find('div', attrs={'class':'w_top_left'})
        read = w_top_left.find_all('dd', attrs={'class':'dd_num'})[0]
        read = read.text.strip()

        try:
            #self.boarddao.save_posts(str(link), str(date), str(title), str(content), str(read))

            with codecs.open('dcinside_g6.csv','a','utf-8') as fa:
                print(date)
                writer = csv.writer(fa)
                writer.writerow([str(link), str(date), title, str(content), str(read), datetime.datetime.now()])

        except Exception, e:
            print e


# class BbasakPostsCrawler(object):
#     def __init__(self, bbasakdao):
#         self.bbasakdao = bbasakdao
#
#     def get_page(self, type, start, end):
#         no = 1
#         while True:
#             url = 'http://bbasak.com/bbs/board.php?bo_table=b001&sfl=wr_subject%7C%7Cwr_content&stx={}&sop=and&page={}'.format(type, no)
#             data = requests.get(url)
#             content = data.content
#             soup = BeautifulSoup(content, 'html5lib')
#             table = soup.find(find_table)
#
#             if len(table.find_all('tr')) == 1:
#                 break
#
#
#             for tr in table.find_all('tr'):
#                 td = tr.find('td', attrs={'class':'tit'})
#                 a = td.find('a')
#                 link = a['href']
#
#
#                 self.crawl_everything(link, type, start, end)
#
#
#             no += 1
#
#     def crawl_everything(self, link, type, start, end):
#         res = requests.get(link)
#         content = res.text
#
#         soup = BeautifulSoup(content, 'html5lib')
#
#         for script in soup(['script', 'style']):
#             script.extract()
#
#         view_title = soup.find('div', attrs={'class':'view_title_txt'})
#
#         title = view_title.find('p', attrs={'class':'tit'})
#         if title == None or title =='':
#             return
#         title = title.text.strip()
#         title = re.sub(',', '', title)
#
#         span = view_title.find_all('span', attrs={'class':'fwb'})
#         date = span[1].text
#         read = span[2].text
#         read = re.sub(',','',read)
#
#         content = soup.find('div', attrs={'class','detailTxt'})
#         content = " ".join(content.text.split())
#         content = re.sub(',','',content)
#
#         date = re.sub(r'(\d{2})-(\d{2})-(\d{2}) (\d{2}):(\d{2})', r'\1,\2,\3,\4,\5', date)
#         end = re.sub(r'(\d{2})-(\d{2})-(\d{2}) (\d{2}):(\d{2})', r'\1,\2,\3,\4,\5', end)
#         start = re.sub(r'(\d{2})-(\d{2})-(\d{2}) (\d{2}):(\d{2})', r'\1,\2,\3,\4,\5', start)
#         print(date)
#         if (datetime.datetime(date) <= datetime.datetime(end)) | (datetime.datetime(date) >= datetime.datetime(start)):
#             try:
#                 # self.bbasakdao.save_posts(str(link), str(date), str(title), str(content), str(read))
#
#                 with codecs.open('bbasak_{}.csv'.format(type),'a','utf-8') as fa:
#                     print(date)
#                     writer = csv.writer(fa)
#                     writer.writerow([str(link), str(date), title, str(content), str(read), datetime.datetime.now()])
#             except Exception, e:
#                 print e
#         else:
#             pass


dcdao = DcDAO()
crawler = DCinsidePostsCrawler(dcdao)
pos_g6 = -4460000
while pos_g6 >= -4500000:
    crawler.get_page(pos_g6,'g6')
    pos_g6 -= 10000


# bbasakdao = BbasakDAO()
# crawler = BbasakPostsCrawler(bbasakdao)
# crawler.get_page('s7', '160110', '160710')
