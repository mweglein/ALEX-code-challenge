from scrapy.spiders import Spider
from alex_challenge.items import AlexChallengeItem
from scrapy.http import Request
import re

class MySpider(Spider):

    name = "courseSpider"
    allowed_domains = ["hws.edu"]
    start_urls = ["http://www.hws.edu/catalogue/courses.aspx"]

    def parse(self, response):

        links = response.xpath("//div[@id='column1wide']/div[@class='box']/p/a/@href").extract()
        crawledLinks = []
        linkPattern = re.compile("^(\S+.aspx)")

        for link in links:
                if linkPattern.match(link) and not link in crawledLinks:
                        link = "http://www.hws.edu/catalogue/" + link
                        yield Request(link, callback=self.parseSubject)


    def parseSubject(self, response):

        titles = response.xpath('//p').re(r'[A-Z]{3,4}[a-z]?\s?\d{3}\s?<strong>.+<\/strong>.*[^<\/p>]')

        for course in titles:

            regex = re.compile("(\S{3,4} \d{3}) <strong>(.+)<\/strong> (.+)", re.UNICODE)
            fields = regex.match(course)

            if fields:

                numberField = fields.group(1).encode('ascii', 'ignore')
                nameField = fields.group(2).encode('ascii', 'ignore')
                descriptionField = fields.group(3).encode('ascii', 'ignore')

                item = AlexChallengeItem()
                item["courseNumber"] = numberField
                item["courseName"] = nameField
                item["courseDescription"] = descriptionField
                yield item

