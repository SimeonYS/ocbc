import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import OocbcItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class OocbcSpider(scrapy.Spider):
	name = 'ocbc'
	start_urls = ['https://www.ocbc.com/group/media/release/index?category=alltopics']

	def parse(self, response):
		post_links = response.xpath('//a[contains(text(),"Read")]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//div[@class="com__ar-de-tags pt3 pb3 fz-14 d-block d-sm-flex align-items-center justify-content-between"]/ul/li/text()').get()
		title = response.xpath('//h3//text()').get()
		content = response.xpath('//div[@class="com__paragraph bp-img wide"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=OocbcItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
