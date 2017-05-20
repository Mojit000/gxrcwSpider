# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GxrcwItem(scrapy.Item):
    # define the fields for your item here like:
    job_name = scrapy.Field()
    job_url = scrapy.Field()
    job_company = scrapy.Field()
    job_salary = scrapy.Field()
    job_address = scrapy.Field()
    job_update_time = scrapy.Field()
    job_recruiting_numbers = scrapy.Field()
    job_education = scrapy.Field()
    job_experience = scrapy.Field()
    job_company_nature = scrapy.Field()
    job_desc_need = scrapy.Field()
    company_desc = scrapy.Field()

# class JobDetailItem(scrapy.Item):
#     job_desc_need = scrapy.Field()
#     company_desc = scrapy.Field()