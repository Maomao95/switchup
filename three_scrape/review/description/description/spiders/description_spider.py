# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from description.items import DescriptionItem
import re
import math
import pandas as pd

def expand_list(nested_list):
		for item in nested_list:
			if isinstance(item, (list, tuple)):
				for sub_item in expand_list(item):
					yield sub_item
			else:
				yield item
link = pd. read_csv('bootcamp.csv')
first_step = list(map(lambda x: x.replace('[','').replace(']','').split(','), link['bootcamp_name']))
second_step = list(expand_list(first_step))
last_step = list(map(lambda x: x.replace("'",'').strip(' '),second_step))
last_step = list(dict.fromkeys(last_step))
loop_lst=[link for link in last_step]

class DescriptionSpider(Spider):
	name = 'Description_spider'
	allowed_urls = ['https://www.switchup.org']
	start_urls = ['https://www.switchup.org' + link for link in loop_lst]

	def parse(self, response):

		pages = response.xpath('//span[@itemprop="reviewcount"]/text()').extract_first()
		pages = re.findall('\d+', pages)[0]
		pages = math.ceil(int(pages)//20)
		review_page_urls = [response.url+'?mobile=false&page=' + str(page) for page in range(1, pages + 1)]
		for url in review_page_urls:
			yield Request(url, callback=self.parse_review_page)

	def parse_review_page(self, response):

		modules = response.xpath('//div[@class="review-block"]')
		bootcamp_name = str(response.xpath('//h1[@class="bootcamp-title"]/text()').extract_first().strip())

		for module in modules:
				reviewer_name = str(module.xpath('.//h3[@class="reviewer-name"]/text()').extract_first().strip())
				try:
					reviewer_title = module.xpath('.//h4[@class="reviewer-title"]/text()').extract()
					reviewer_title = list(map(lambda x: x.strip(), reviewer_title))
				except:
					reviewer_title = ''
				date = module.xpath('.//time[@itemprop="datepublished"]/@datetime').extract_first()

				try:
					overall_score = module.xpath('.//div[@class="review-scores-overall"]//div[@class="rating-stars--fill"]/@style').extract()[0]
					overall_score = float(re.findall(r'\d+\.\d+',overall_score)[0])
				except:
					overall_score = ''

				try:
					curriculum_score = module.xpath('.//div[@class="review-scores-curriculum"]//div[@class="rating-stars--fill"]/@style').extract()[0]
					curriculum_score = float(re.findall(r'\d+\.\d+',curriculum_score)[0])
				except:
					curriculum_score = ''
				try:
					job_support_score = module.xpath('.//div[@class="review-scores-career"]//div[@class="rating-stars--fill"]/@style').extract()[0]
					job_support_score = float(re.findall(r'\d+\.\d+',job_support_score)[0])
				except:
					job_support_score = ''
				try:
					review_title = str(module.xpath('.//h4[@class="review-headline"]/text()').extract_first())
				except:
					review_title = ''

				try:
					review_content = str(module.xpath('.//a[@class="read-more"]/@onclick').extract_first())
				except:
					review_content = str(module.xpath('.//span[@itemprop="description"]/p/text()').extract_first())

				item = DescriptionItem()
				item['bootcamp_name'] = bootcamp_name
				item['reviewer_name'] = reviewer_name
				item['reviewer_title'] = reviewer_title
				item['date'] = date
				item['overall_score'] = overall_score
				item['curriculum_score'] = curriculum_score
				item['job_support_score'] = job_support_score
				item['review_title'] = review_title
				item['review_content'] = review_content
				yield item