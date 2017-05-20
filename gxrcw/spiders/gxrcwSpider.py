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
            # Items对象是可变类型,内容改变后地址保持不变
            # 如果放在for循环外面的话,jobsItem实例一直指向同一个地址
            # 即在meta参数传递的都是指向同一个地址的jobsItem实例,只是内容改变了,以前的内容会被新的内容覆盖
            # 只有每次重新执行parse_jobs()方法后,jobsItem实例指向的地址才会发生变化
            # 所以放在for循环外面得到的数据第一部分只有三种结果,就是每一页最后一项的结果
            jobItem = GxrcwItem()
            # 抓取一部分数据
            jobItem['job_name'] = job.css('ul.posDetailUL.clearfix > li.w1 > h3 > a::text').extract_first()
            jobItem['job_url'] = job.css('ul.posDetailUL.clearfix > li.w1 > h3 > a::attr(href)').extract_first()
            jobItem['job_company'] = job.css('ul.posDetailUL.clearfix > li.w2 > a::text').extract_first()
            jobItem['job_salary'] = job.css('ul.posDetailUL.clearfix > li.w3::text').extract_first()
            jobItem['job_address'] = job.css('ul.posDetailUL.clearfix > li.w4::text').extract_first()
            jobItem['job_update_time'] = job.css('ul.posDetailUL.clearfix > li.w5::text').extract_first()
            job_detail= [i for i in zip(job.css('ul.qitaUL > li > strong::text').extract(), job.css('ul.qitaUL > li > span::text').extract())]
            jobItem['job_recruiting_numbers'] = job_detail[0]
            jobItem['job_education'] = job_detail[1]
            jobItem['job_experience'] = job_detail[2]
            jobItem['job_company_nature'] = job_detail[3]
            yield scrapy.Request(url=jobItem['job_url'], callback=self.parse_job_detail, meta={'jobs':jobItem})

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
        jobsItem['job_desc_need'] = '\n'.join(job_desc_need).strip()
        jobsItem['company_desc'] = response.css('#content > div.gsR_con > div.gz_info > p::text').extract_first().strip()
        return jobsItem
        
