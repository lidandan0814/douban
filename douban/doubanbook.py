import requests
from pyquery import PyQuery as pq
import json
import time
from openpyxl import Workbook
lines = []

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


def parse_html(html):
    doc = pq(html)
    items = doc.find('.subject-list li').items()
    for item in items:
        book = {}
        book['书名'] = item.find('.info h2 a').text()
        book['价格'] = item.find('.info .pub').text().split('/')[-1]
        book['出版日期'] = item.find('.info .pub').text().split('/')[-2]
        book['出版社'] = item.find('.info .pub').text().split('/')[-3]
        book['作者'] = item.find('.info .pub').text().split('/')[0]
        book['评分'] = item.find('.info .star .rating_nums').text()
        book['评价人数'] = item.find('.info .star .pl').text()
        book['评论摘要'] = item.find('.info p').text()
        #print(book)
        booklist = [book['书名'], book['价格'], book['出版日期'], book['出版社'],
            book['作者'], book['评分'], book['评价人数'], book['评论摘要']]
        lines.append(booklist)
    return lines


def write_to_file(result):
    #保存到Excel
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(['书名','价格', '出版日期', '出版社', '作者','评分', '评价人数', '评论摘要'])
    for line in lines:
        worksheet.append(line)
    workbook.save('豆瓣编程书籍清单.xlsx')
    #保存为txt格式
#    with open('result.txt', 'a', encoding='utf-8') as f:
#        f.write(json.dumps(result, ensure_ascii=False) + '\n')


def main(offset):
    print('第', i + 1 , '页')
    url = 'https://book.douban.com/tag/%E7%BC%96%E7%A8%8B?start=' + str(offset) + '&type=T'
    html = get_html(url)
    for lines in parse_html(html):
        write_to_file(lines)


if __name__ == '__main__':
    for i in range(15):
        main(offset=i * 20)
        time.sleep(10)
