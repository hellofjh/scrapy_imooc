# spider/imooc.py
# -*- coding: utf-8 -*-
import json

import scrapy
from imooc_spider.items import ImoocSpiderItem

class ImoocSpider(scrapy.Spider):
    # 必须唯一
    name = 'imooc'
    # 允许爬取的域名列表
    allowed_domains = ['www.imooc.com']
    # 第一个被获取到的页面的URL将是该列表之一,后续的URL将会从获取到的数据中提取
    start_urls = ['https://www.imooc.com/course/list?c=be&page=1']

    # 当response没有指定回调函数时，该方法是Scrapy处理下载的response的默认方法。
    def parse(self, response):
        print(response.request.headers)
        # print(response.body)  # 查看是否请求成功

        course_card_list = response.xpath("//div[@class='course-card-container']")
        for item in course_card_list:
            info = {}
            # extract / extract_first: list数据 / list第一条数据
            info['course_name'] = item.xpath(".//h3[@class='course-card-name']/text()").extract_first()
            info['course_desc'] = item.xpath(".//p[@class='course-card-desc']/text()").extract_first()
            info['course_url'] = "https://www.imooc.com" + item.xpath("./a/@href").extract_first()
            info['course_img_urls'] = "https:" + item.xpath('.//img/@data-original').extract_first()
            yield info
            # 我们使用yield来发送这个异步请求
            # 使用的是scrapy.Request发送请求的
            # 回调函数,只写方法的名称，不要调用方法
        #     yield scrapy.Request(url=info['course_url'], callback=self.handle_detail_page, meta=info)
        #
        # next_run = response.xpath("//*[@id='main']//div[@class='page']/span[@class='disabled_page']/text()").extract()
        # if "下一页" not in next_run:
        #     active_page = response.xpath(
        #         "//*[@id='main']//div[@class='page']/a[contains(@class, 'active text-page-tag')]/text()").extract_first()
        #     next_page = "https://www.imooc.com/course/list?c=be&page={}".format(int(active_page) + 1)
        #     yield scrapy.Request(url=next_page, callback=self.parse)

    def handle_detail_page(self, response):
        chapter_list = response.xpath('//div[contains(@class,"chapter course-wrap")]/ul[@class="video"]/li/a')
        info = ImoocSpiderItem()
        info['course_name'] = response.request.meta['course_name']
        info['course_desc'] = response.request.meta['course_desc']
        info['course_url'] = response.request.meta['course_url']
        info['course_img_urls'] = response.request.meta['course_img_urls']
        info['teacher_name'] = response.xpath(
            '//div[contains(@class, "teacher-info")]/span[@class="tit"]/a/text()').extract_first()
        video_lists = []
        for item in chapter_list:
            video_lists.append("https://www.imooc.com" + item.xpath(".//@href").extract_first())

        info['video_url_list'] = video_lists
        yield info
