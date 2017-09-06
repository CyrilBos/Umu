# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Spider



class MailParser(Spider):
    name = "MailParser"
    mails = []

    def start_requests(self):
        urls = [
                'file:///home/cyrbos/Downloads/cambro-roster.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        print("PARSING PAGE: " + response.url)
        table = response.css('div#roster-members')
        for row in table.css('div.roster-member'):
            columns = row.css('div.roster-table-cell')
            role = columns.extract()[3].strip().splitlines()[2].strip()
            if role == 'Student':
                mail = columns.xpath('.//a/text()').extract()[2].strip()
                mail = mail[:mail.index('@')+1] + 'student.umu.se'
                self.mails.append(mail)

        str = ""
        for mail in self.mails:
            str += mail + ';'
        str = str[:len(str)-1]
        print(str)
        print(len(self.mails))