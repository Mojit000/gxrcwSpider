# -*- coding: utf-8 -*-
import scrapy
from gxrcw.items import GxrcwItem
# from gxrcw.items import JobDetailItem

class GxrcwspiderSpider(scrapy.Spider):
    name = "gxrcwSpider"
    # allowed_domains = ["gxrc.com"]
    start_urls = ['http://s.gxrc.com/sJob?schType=1&pageSize=20&orderType=0&listValue=1&keyword=Python&page=1',]


    def parse(self, response):
        for url in GxrcwspiderSpider.start_urls:
            yield scrapy.Request(url, callback=self.parse_jobs)


    def parse_jobs(self, response):
        # jobsItems = []
        jobs = response.css('div.rlOne')
        for job in jobs:
            jobsItem = GxrcwItem()
            # 抓取一部分数据
            jobsItem['job_name'] = job.css('ul.posDetailUL.clearfix > li.w1 > h3 > a::text').extract_first()
            jobsItem['job_url'] = job.css('ul.posDetailUL.clearfix > li.w1 > h3 > a::attr(href)').extract_first()
            jobsItem['job_company'] = job.css('ul.posDetailUL.clearfix > li.w2 > a::text').extract_first()
            jobsItem['job_salary'] = job.css('ul.posDetailUL.clearfix > li.w3::text').extract_first()
            jobsItem['job_address'] = job.css('ul.posDetailUL.clearfix > li.w4::text').extract_first()
            jobsItem['job_update_time'] = job.css('ul.posDetailUL.clearfix > li.w5::text').extract_first()
            job_detail= [i for i in zip(job.css('ul.qitaUL > li > strong::text').extract(), job.css('ul.qitaUL > li > span::text').extract())]
            jobsItem['job_recruiting_numbers'] = job_detail[0]
            jobsItem['job_education'] = job_detail[1]
            jobsItem['job_experience'] = job_detail[2]
            jobsItem['job_company_nature'] = job_detail[3]
            yield scrapy.Request(url=jobsItem['job_url'], callback=self.parse_job_detail, meta={'jobs':jobsItem})

        # 分页递归爬取
        # 思路:找到下一页按钮的链接,重新爬取
        # 递归爬取终结条件:下一页按钮不存在
        next_page = 'http://s.gxrc.com/sJob' + response.css('ul.pagination > li.PagedList-skipToNext > a::attr(href)').extract_first() if response.css(
            'ul.pagination > li.PagedList-skipToNext > a::attr(href)') else None
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_jobs)

    def parse_job_detail(self, response):
        # 抓取另外一部分数据
        jobsItem = response.meta['jobs']
        jobsItem['job_url'] = response.url
        job_desc_need = response.css('#content > div.gsR_con > div.gsR_con_txt > div > div.gz_info_txt > p::text').extract()
        jobsItem['job_desc_need'] = '\n'.join(job_desc_need)
        jobsItem['company_desc'] = response.css('#content > div.gsR_con > div.gz_info > p::text').extract_first()
        return jobsItem
        
