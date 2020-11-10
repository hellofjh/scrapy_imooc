# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImoocSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    course_name = scrapy.Field()  # 课程名
    course_desc = scrapy.Field()  # 课程描述
    course_url = scrapy.Field()  # 课程链接
    course_img_urls = scrapy.Field()  # 课程图片链接
    teacher_name = scrapy.Field()  # 下一层请求课程链接后取得：讲师名
    video_url_list = scrapy.Field()  # 下一层请求课程链接后取得：章节视频
