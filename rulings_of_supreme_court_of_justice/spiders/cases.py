import scrapy
from scrapy.loader import ItemLoader
from ..items import RulingsOfSupremeCourtOfJusticeItem
from ..pipelines import check_links_in_database
from scrapy.exceptions import CloseSpider

class CasesSpider(scrapy.Spider):
    name = "cases"

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    def start_requests(self):
        yield scrapy.Request(
            url="http://www.dgsi.pt/jstj.nsf?OpenDatabase",
            headers=self.HEADERS,
            callback=self.parse
        )

    def parse(self, response):
        for links in response.xpath('(//table)[2]//font/a/@href').getall():
            
            ########################### DEFAULT LOGIC STOPS WHEN IT SEES A PAGE WITH ALL THE LINKS IN DATABASE ##########################
            #if response.request.url != 'http://www.dgsi.pt/jstj.nsf?OpenDatabase':
                #Checking links on each page and seeing if they are already in the database if so then spider stops
                #homepage_links = response.xpath('(//table)[2]//font/a/@href').getall()
                #check if all the links in homepage_links are already in our database if they are all in the database Raise the CloseSpider exception from a callback
                #if check_links_in_database(homepage_links):
                    #raise CloseSpider("All links are in the database. Stopping execution.")
            #############################################################################################################################


            ########### IF YOU HAVE COMPLETED SCRAPING DATABASE (uncomment code below)  CHECKS FOR NEW ITEMS IF NOT STOPS #########################
            #homepage_links = response.xpath('(//table)[2]//font/a/@href').getall()
            #if check_links_in_database(homepage_links):
                #raise CloseSpider("All links are in the database. Stopping execution.")
            ####################################################################################################
            
            #getting the dates
            dates = response.xpath('(//table)[2]//tr/td[1]//font/text()').getall()

            link = f"http://www.dgsi.pt{links}"
            date = dates[response.xpath('(//table)[2]//font/a/@href').getall().index(links)]
            yield scrapy.Request(
                url=link,
                headers=self.HEADERS,
                callback=self.parse_docs,
                meta={
                    'date':date
                }
            )
        
        # Code for handling the pagination of the website
        urls = response.xpath('(//tr)[108]//a//font/text()').getall()
        for items in urls:
            if items == 'Seguinte':
                url = response.xpath(f'(//tr)[108]//a[{urls.index(items)+1}]/@href').get()
                absolute_url = f'http://www.dgsi.pt{url}'
                yield scrapy.Request(
                    url= absolute_url,
                    headers=self.HEADERS,
                    callback=self.parse
                )
    
    def parse_docs(self,response):
        l = ItemLoader(item=RulingsOfSupremeCourtOfJusticeItem(), response=response)
        
        #getting total length of data points
        labels = response.xpath('(//table)[1]//td[1]//font[@color="#FFFFFF"]//text()').getall()
        document_data = {}

        for i in range(len(labels)):
            name = response.xpath(f'((//table)[1]//td[1]//font[@color="#FFFFFF"])[{i+1}]//text()').get()

            if name == 'Sumário :':
                value = response.xpath(f'((//table)[1]//td[2]//font[@color="#000080"])[{i+1}]').extract()
                document_data[name] = value
            elif name == 'Decisão Texto Integral:':
                value = response.xpath(f'((//table)[1]//td[2]//font[@color="#000080"])[{i+1}]').extract()
                document_data[name] = value
            else:
                value = response.xpath(f'((//table)[1]//td[2]//font[@color="#000080"])[{i+1}]//text()').extract()
                document_data[name] = value
        
        l.add_value('document_contents', document_data)
        #getting the link
        l.add_value('link', response.request.url)
        #getting the date
        l.add_value('date',response.meta.get('date'))

        item = l.load_item()
        yield item  