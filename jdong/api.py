# -*- coding: utf-8 -*-

import re
import requests
from lxml import etree

from .utils import *


class JDong(object):
    def __init__(self):
        pass

    def search(self, keyword, page=1):
        """搜索
        """
        url = 'https://search.jd.com/Search?keyword={}&enc=utf-8&page={}'.format(keyword, page)
        r = get(url)
        html = etree.HTML(r)
        goodslist = html.xpath('//*[@id="J_goodsList"]/ul/li')
        relist = []
        for goods in goodslist:
            link = goods.xpath('div/div[1]/a/@href')
            img = goods.xpath('div/div[1]/a/img/@src')
            price_type = goods.xpath('div/div[3]/strong/em/text()')
            price_data = goods.xpath('div/div[3]/strong/i/text()')
            name = goods.xpath('div/div[4]/a/@title')
            comment = goods.xpath('div/div[5]/strong/a/text()')
            uid = re.findall('jd.com/(.*?).html', link[0]) if link else None

            if uid:
                uid = uid[0]
                link = 'http:{}'.format(link[0]) if link else ''
                img = 'http:{}'.format(img[0]) if img else ''
                price_type = price_type[0] if price_type else ''
                price_data = price_data[0] if price_data else ''
                name = name[0] if name else ''
                comment = comment[0] if comment else ''
                relist.append({
                    'uid': uid,
                    'link': link,
                    'img': img,
                    'price_type': price_type,
                    'price_data': price_data,
                    'name': name,
                    'comment': comment
                })
        return relist

    def comment(self, product_id, page=1):
        """评论
        """
        url = 'https://sclub.jd.com/comment/productPageComments.action?productId={}&score=0&sortType=3&' \
              'page={}&pageSize=10&callback=fetchJSON_comment98vv157'.format(product_id, page)
        r = get(url)
        data = re.findall('fetchJSON_comment98vv157\((.*?)\);', r)
        data = data[0]
        data = data.replace('null', '\'null\'')
        data = data.replace('false', '\'false\'')
        data = data.replace('true', '\'true\'')
        data = eval(data)
