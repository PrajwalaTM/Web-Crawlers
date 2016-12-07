import scrapy,urlparse
from scrapy.spiders import Spider
from Pokemon.items import PokemonItem
from scrapy.http    import Request
import re
from urlparse import urljoin
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector

class PokemonSpider(Spider):

	name= "Pokemon"
	allowed_domains=["pokemondb.net"]
	start_urls=["http://pokemondb.net/pokedex/national"]
	

	def parse(self,response):
		title=response.xpath('//a/@href').extract()[-1]
		links = response.xpath('//a/@href').extract()
		linkpattern=re.compile("^\/pokedex\/+")
		seen_urls=[]
		for link in links:
			#print("Link is"+str(link))
			#hxs = Selector(text="http://pokemondb.net"+link)
			#sublink=hxs.xpath('//@src').extract()
			#print(sublink)
			if linkpattern.match(link) and not ("http://pokemondb.net"+link) in seen_urls:
				link="http://pokemondb.net"+link
				seen_urls.append(link)
				yield Request(link,self.parse)

		imageurls=response.xpath('//@src').extract()
		for url in imageurls:
			if (url.endswith('.jpg')):
				obj=PokemonItem()
				obj['page_title']=title
				obj['image_urls']=[response.urljoin(url)]
				yield obj
			