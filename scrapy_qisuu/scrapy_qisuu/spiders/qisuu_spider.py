# -*- coding: utf-8 -*-
import scrapy
from scrapy_qisuu.items import ScrapyQisuuItem


class QisuuSpiderSpider(scrapy.Spider):
    name = 'qisuu_spider'
    allowed_domains = ['qisuu.la']
    main_url = ['http://www.qisuu.la']
    start_urls = ['https://www.qisuu.la/soft/sort010/']

    def parse(self, response):
        # qisuu=response.css('div.nav')
        end_page = response.css('div.tspage').css('a::attr(href)').extract()[-1]
        all_page = end_page.split('_')[1].split('.')[0]
        for page in range(1,int(all_page)+1):
            # https: // www.qisuu.la / soft / sort06 / index_2.html
            url = self.main_url[0] +'/soft/sort010/index_' + str(page)+ '.html'
            request = scrapy.Request(url, callback=self.parse_next)
            yield request
    def parse_next(self,response):
        for i in response.css('div.listBox li'):
            list =i.css("a ::attr(href) ").extract()
            for link in list:
                if link.endswith('.html'):
                    book_url = self.main_url[0] + link
                    #print(url)
                    yield scrapy.Request(book_url, callback=self.parse_item)

    def parse_item(self,response):
        # l = ItemLoader(item=CoserItem(), response=response)
        books = ScrapyQisuuItem()
        #书的下载页
        for book in response.css('div.detail_info'):
            books['name'] = book.css('h1::text').extract()[0]
            books['author'] = book.css('li::text').extract()[5]
            # print('书名: %s 作者: %s'%(name ,author))

        book_list = response.css('div.showDown script').extract()
        if book_list:
            books['url'] = book_list[0].split(',')[1][1:-1:]
        # self.log('url %s' % books)
        yield books





