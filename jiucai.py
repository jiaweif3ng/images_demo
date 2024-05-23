import concurrent
import datetime
import re
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List
from lxml import etree
from config import jiucai_config

# from fin_spider.config.global_config import jiucai_config
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service


class JiuCaiSpider:
    def __init__(self) -> None:
        firefox_options = Options()
        firefox_options.binary_location=jiucai_config["firefox_binary_location"]
        firefox_options.add_argument('-headless')
        firefox_options.add_argument('--disable-gpu')
        # 不加载图片
        firefox_options.add_argument('blink-settings=imagesEnabled=false')
        # requests不能正常获取到页面元素，所以用selenium库
        service = Service(jiucai_config["geckodriver_path"])
        self.bro = webdriver.Firefox(options=firefox_options, service=service)

    def _get_title(self, li):
        try:
            title = li.xpath('./div/section/div[2]/div/div/span//text()')[0]
        except:
            title = ''
        return title

    def _get_author_name(self, li):
        try:
            author = li.xpath('./div/section/div[1]/div[1]/div/div[2]/div[1]/div[1]/span//text()')[0]
        except:
            author = ''
        return author

    def _get_forward_num(self, li):
        try:
            forward_num = li.xpath('./div/section/div[3]/div/div[2]/div[1]/span//text()')[0]
        except:
            forward_num = ''
        return forward_num

    def _get_reply_num(self, li):
        try:
            reply_num = li.xpath('./div/section/div[3]/div/div[2]/div[2]/span//text()')[0]
        except:
            reply_num = ''
        return reply_num

    def _get_likes_num(self, li):
        try:
            likes_num = li.xpath('./div/section/div[3]/div/div[2]/div[3]/span//text()')[0]
        except:
            likes_num = ''
        return likes_num

    def _get_referer(self, li):
        detailed_url = 'https://www.jiuyangongshe.com' + li.xpath('./div/section/div[3]/div/section/div/div/a//@href')[0]
        return detailed_url

    def _process_gbk(self, content:str) -> str:
        '''
        去掉无法识别的字符
        :param content: 要处理的内容
        :return: 处理后的内容
        '''
        content = re.sub(u'([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b])', '', content)
        return content

    def _get_content(self, url:str) -> List:
        l = []
        self.bro.get(url)
        response = self.bro.page_source
        tree = etree.HTML(response)
        try:
            time = tree.xpath('//*[@id="__layout"]/div/div[2]/div/div[1]/div[2]/div/div/div[2]//text()')[0]
        except:
            time = ''
        l.append(time)
        try:
            #content = tree.xpath('//*[@id="__layout"]/div/div[2]/div/div[1]/section/div[1]/div[1]//text()')
            content = tree.xpath('//*[@id="__layout"]/div/div[2]/div/div[1]/section/div[1]//text()')
            content = ','.join(content)
            content = self._process_gbk(content)
        except:
            content = ''
        l.append(content)
        return l

    def is_within_days(self, date_str, n):
        try:
            date = datetime.datetime.strptime(date_str.strip(), '%Y-%m-%d %H:%M:%S')
            n_days_ago = datetime.datetime.now() - datetime.timedelta(days=n)
            return date > n_days_ago
        except:
            return False

    def get_jiucai_data(self, query:str, items_num:int) -> List[Dict]:
        page_url = f'https://www.jiuyangongshe.com/search/new?k={query}'
        self.bro.get(page_url)
        page_response = self.bro.page_source
        #print(page_response)
        page_tree = etree.HTML(page_response)
        li_list = page_tree.xpath('//*[@id="container"]/div[5]/div/ul/li')
        jiucai_data = []
        for li in li_list[:items_num]:
            referer = self._get_referer(li)
            data_info = {
                'title': self._get_title(li),
                'author': self._get_author_name(li),
                'forward_num': self._get_forward_num(li),
                'reply_num': self._get_reply_num(li),
                'likes_num': self._get_likes_num(li),
                'time': self._get_content(referer)[0],   # 格式为 '2024-04-27 10:46:00 '
                'content': self._get_content(referer)[1]
            }
            #print(data_info)
            if self.is_within_days(data_info["time"], jiucai_config["recent_day"]):
                jiucai_data.append(f"{data_info['title']}: {data_info['content']}")
        return str(jiucai_data)

if __name__ == '__main__':
    api = JiuCaiSpider()
    data_list = api.get_jiucai_data('永冠新材', 3)
    print(data_list)