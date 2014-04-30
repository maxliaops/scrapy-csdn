import re
import json

from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from scrapy import log

from CsdnColumn.items import *
from CsdnColumn.misc.log import *

class E21jobSpider(CrawlSpider):
    name = "CsdnColumn"
    allowed_domains = ["blog.csdn.net"]
    start_urls = [
        "http://blog.csdn.net/all/column/list.html"
    ]
    rules = [
        Rule(sle(allow=("/column/details/.*.html", )), callback='parse_detail'),
        Rule(sle(allow=("/all/column/list.html\?page=\d{,2}")), follow=True, callback='parse_list')
    ]

    def parse_detail(self, response):
        items = []
        sel = Selector(response)
        base_url = get_base_url(response)
        item = ColumnItem()
        item['detailLink'] = response.url

        array = sel.css('#col_tit::text').extract()
        if len(array) == 1 :
            item['colTitle'] = array[0]
        else :
            item['colTitle'] = ""

        array = sel.css('div.main_right').css('div:nth-child(1)').css('li:nth-child(2)::text').extract()
        if len(array) == 1 :
            item['createTime'] = array[0]
        else :
            item['createTime'] = ""

        array = sel.css('div.main_right').css('div:nth-child(1)').css('li:nth-child(3)::text').extract()
        if len(array) == 1 :
            item['articleNum'] = array[0]
        else :
            item['articleNum'] = ""

        array = sel.css('div.main_right').css('div:nth-child(1)').css('li:nth-child(4)::text').extract()
        if len(array) == 1 :
            item['views'] = array[0]
        else :
            item['views'] = ""

        array = sel.css('div.main_right').css('div:nth-child(1)').css('li:nth-child(1)').css('a::text').extract()
        if len(array) == 1 :
            item['author'] = array[0]
        else :
            item['author'] = ""

        array = sel.css('div.main_right').css('div:nth-child(1)').css('li:nth-child(1)').css('a').xpath('@href').extract()
        if len(array) == 1 :
            item['authorLink'] = array[0]
        else :
            item['authorLink'] = ""

        array = sel.css('#col_desc::text').extract()
        if len(array) == 1 :
            item['colDesc'] = array[0]
        else :
            item['colDesc'] = ""

        items.append(item)
        info('parsed ' + str(response))
        return items

    def parse_list(self, response):
        info('parsed ' + str(response))

    def _process_request(self, request):
        info('process ' + str(request))
        return request

