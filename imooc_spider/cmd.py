#!/usr/bin/env python
# -*- coding:utf-8 -*-
from scrapy import cmdline
# 方式一：注意execute的参数类型为一个列表
cmdline.execute('scrapy crawl imooc'.split())
# cmdline.execute('scrapy crawl imooc -o items.json'.split())