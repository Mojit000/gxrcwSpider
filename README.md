# 广西人才网爬虫  gxrcwSpider
     
## 参考资料       
1. [Scrapy分页爬取四川大学公共管理学院全职教师信息及学院新闻](http://www.jianshu.com/p/ad6bf3f2a883#)             
2. [Scrapy抓取在不同级别Request之间传递参数](http://www.jianshu.com/p/de61ed0f961d)

## Bug修复说明
```
# 错误的代码
def parse_jobs(self, response):
        # jobsItems = []
        jobs = response.css('div.rlOne')
        jobsItem = GxrcwItem()
        for job in jobs:
            # 抓取一部分数据
```

```
# 正确的代码
def parse_jobs(self, response):
        # jobsItems = []
        jobs = response.css('div.rlOne')
        for job in jobs:
            jobsItem = GxrcwItem()
            # 抓取一部分数据
```

## Bug分析
