# spider/testProxy.py
# -*- coding: utf-8 -*-
import scrapy

class testProxy(scrapy.Spider):
    name = 'test_proxy'
    allowed_domains = ['tool.lu']
    start_urls = ['https://tool.lu/ip']

    def parse(self, response):
        # 取到检测IP的网页关键元素
        your_ip_list = response.xpath("//*[@id='main_form']/p[1]/text()").extract_first()
        print(your_ip_list)
