import sys
#print sys.path
import os
sys.path.append(os.getcwd())
from scrapy import Selector 
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from quotes.items import QuoteItem

def safe_extract(selector): 	
	try: 		
		return selector[0].extract().strip() 	
	except IndexError: 		
		return None   

class QuotesSpider(CrawlSpider): 	
	name = "quotes_spider"  	
	start_urls = ['https://www.goodreads.com/quotes?page=1']  	
	rules = [
		Rule(LinkExtractor(allow=('https?://www.goodreads.com/quotes.*', )), callback='extract'),
	]  	

def extract(self, response): 		
	selector = Selector(response)  		
	q = QuoteItem()  		
	q["url"] = response.url 		
	q["name"] = safe_extract(selector.css("div.hotel_id h1 span[itemprop='name']::text")) 	
	q["streetAddress"] = safe_extract(selector.css("div.hotel_id ul.hotel_address span[itemprop='streetAddress']::text"))

	yield q
