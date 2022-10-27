import scrapy
from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        for link in response.xpath('//*[@id="numerical-index"]'
                                   ).css('tbody').css('tr'):
            pep_link = link.css('a::attr(href)').get()
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        number = response.xpath('//*[@id="pep-page-section"]/header\
            /ul/li[3]/text()').get().split()
        data = {
            'number': number[1],
            'name': response.xpath('//*[@id="pep-content"]/h1/text()').get(),
            'status': response.css('dt:contains("Status") + dd::text').get()
            }
        yield PepParseItem(data)
