import scrapy



class Spider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = []
    start_urls = ['https://s.taobao.com/search?q=%E7%BE%8E%E9%A3%9F']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        titele = response.xpath('//div[@class="row row-2 title"]/a/text()').extract()
        print('这是标题：', titele)

