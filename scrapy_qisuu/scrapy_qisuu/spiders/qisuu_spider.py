# -*- coding: utf-8 -*-
import scrapy
from scrapy_qisuu.items import ScrapyQisuuItem


class QisuuSpiderSpider(scrapy.Spider):
    name = 'qisuu_spider'
    allowed_domains = ['qisuu.la']
    main_url = ['http://www.qisuu.la']
    start_urls = ['https://www.qisuu.la/soft/sort010/']

    def parse(self, response):
        qisuu=response.css('div.nav')
        books = ScrapyQisuuItem()
        for i in qisuu:
            #table =i.css('a::attr(href)').extract()
            urls =i.css('a::attr(href)').extract()
        #书的下载页
        for i in response.css('div.listBox li'):
            list =i.css("a ::attr(href) ").extract()
            for link in list:
                if link.endswith('.html'):
                    book_url = self.main_url[0] + link
                    #print(url)
                    yield scrapy.Request(book_url, callback=self.parse)
        for book in response.css('div.detail_info'):
            books['name'] = book.css('h1::text').extract()[0]
            books['author'] = book.css('li::text').extract()[5]
            # print('书名: %s 作者: %s'%(name ,author))

        book_list = response.css('div.showDown script').extract()
        if book_list:
            books['url'] = book_list[0].split(',')[1][1:-1:]
        self.log('url %s' % books)
        yield books
