# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DescriptionItem(scrapy.Item):
	bootcamp_name = scrapy.Field()
	reviewer_name = scrapy.Field()
	reviewer_title = scrapy.Field()
	date = scrapy.Field()
	overall_score = scrapy.Field()
	curriculum_score = scrapy.Field()
	job_support_score = scrapy.Field()
	review_title = scrapy.Field()
	review_content = scrapy.Field()


