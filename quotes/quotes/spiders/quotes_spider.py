import sys
#print sys.path
import os
sys.path.append(os.getcwd()) # quotes.items is not found for some reason

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from quotes.items import QuoteItem
from pyquery import PyQuery as pq

class QuotesSpider(CrawlSpider): 	
	name = "quotes_spider"  	
	start_urls = ['https://www.goodreads.com/quotes?page=1']  	
	rules = [
		Rule(LinkExtractor(allow=('https?://www.goodreads.com/quotes.*', )), callback='extract'),
	]  	

	def extract(self, response): 		
		pq_document = pq(response.body)  		
		q = QuoteItem()

		for quote_data in pq_document(".quoteDetails").items():
			q["url"] = response.url 		
			q["text"] =  quote_data(".quoteText").clone().remove('a').remove('span').remove('script').text()
			q["author"] = quote_data(".quoteText a").text()

			yield q
