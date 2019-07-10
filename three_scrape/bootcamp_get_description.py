from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
from time import sleep 
import pandas as pd

driver = webdriver.Chrome(r'C:\Users\13917109271\Desktop\bootcamp\python/chromedriver.exe')
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

csv_file = open('description.csv','w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)
for ii in range(len(loop_lst)):
	driver.get("https://www.switchup.org"+ loop_lst[ii])

	description = driver.find_element_by_xpath('//div[@class="bootcamp-caption text-center"]')
	description_dict={}
	try:
		is_not_best_bootcamp = driver.find_element_by_xpath('//div[@class="top-badge-img"]/img').get_attribute('alt')
	except:
		is_not_best_bootcamp = ''
	bootcamp_name = description.find_element_by_xpath('//h1[@class="bootcamp-title"]').text
	raw_score = description.find_element_by_xpath('//div[@class="rating-stars--fill"]').get_attribute('style')
	try:
		general_score = re.findall(r'\d+\.\d+',raw_score)[0]
		general_score = float(general_score)
	except:
		general_score = ''
	review_number = description.find_element_by_xpath('//a[@href="#tablist-tab-review"]').text
	review_number = re.findall(r'\d+',review_number)[0]
	review_number = int(review_number)

	price = len(driver.find_elements_by_xpath('//span[@class="dollar-sign--filled"]'))

	extra_information = driver.find_element_by_xpath('//div[@class="extra-info hidden-phone"]')


	view_mores = driver.find_elements_by_xpath('//a[@href ="#"]')
	for view_more in view_mores[:3]:
		try:
			view_more.click()
		except:
			pass
	location = extra_information.find_elements_by_xpath('//div[@class="extra-info hidden-phone"]//span')[0].text
	programs_available = extra_information.find_elements_by_xpath('//div[@class="extra-info hidden-phone"]//span')[1].text


	index = len(driver.find_elements_by_xpath('//div[@class="extra-info hidden-phone"]//span'))
	if index >= 3:
		scholarships = extra_information.find_elements_by_xpath('//div[@class="extra-info hidden-phone"]//span')[2].text
	else:
		scholarships = ''

	description_dict['is_not_best_bootcamp'] = is_not_best_bootcamp
	description_dict['bootcamp_name'] = bootcamp_name
	description_dict['general_score'] = general_score
	description_dict['review_number'] = review_number
	description_dict['price'] = price
	description_dict['location'] = location
	description_dict['programs_available'] = programs_available
	description_dict['scholarships'] = scholarships
	writer.writerow(description_dict.values())




		


csv_file.close()
driver.close()