# -*- coding: utf-8 -*-
from scrapy import Spider
from bootcamp.items import bootcampItem
import pandas as pd


class bootcampSpider(Spider):
	name = 'bootcamp_spider'
	allowed_urls = ['https://www.switchup.org']
	link = pd. read_csv('bootcamp.csv')
	def expand_list(nested_list):
		for item in nested_list:
			if isinstance(item, (list, tuple)):
				for sub_item in expand_list(item):
					yield sub_item
			else:
				yield item
	first_step = list(map(lambda x: x.replace('[','').replace(']','').split(','), link['bootcamp_name']))
	second_step = list(expand_list(first_step))
	last_step = list(map(lambda x: x.replace("'",'').strip(' '),second_step))
	
	start_urls = ['https://www.switchup.org/all-courses-and-bootcamps?mobile=false&page=' + str(i) for i in range(56)]

	def parse(self, response):
		# Find all the table rows
			bootcamp_name = response.xpath('//a[@class="text-center"]/@href').extract()
			bootcamp_name = unlist(bootcamp_name)
			bootcamp_name = str(bootcamp_name)

			item = bootcampItem()
			item['bootcamp_name'] = bootcamp_name
			yield item
