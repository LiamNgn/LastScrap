from scrapy import Spider
import scrapy

class StackSpider(Spider):
	name = "LastSpider"
	start_urls = [
	"https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html?fbclid=IwAR1ITzR4dR0bPFuaFM-M_WcE67mSzTvHrmNsHzQHn6qsqNuLPQT5qTWP8do",
	]

	def parse(self, response):
		for info in response.xpath("//tr[td[a[contains(text(),'Last Statement')]]]"):
			yield{
			"ID:": info.xpath('td[1]/text()').get(),
			"Last Name": info.xpath('td[4]/text()').get(),
			"First Name": info.xpath('td[5]/text()').get(),
			"TDCJ number": info.xpath('td[6]/text()').get(),
			"Age": info.xpath('td[7]/text()').get(),
			"Date of Execution": info.xpath('td[8]/text()').get(),
			"Race": info.xpath('td[9]/text()').get(),
			"County": info.xpath('td[10]/text()').get(),
			}
		for quotes in response.xpath("//tr[td[a[contains(text(),'Last Statement')]]]"):
			url = response.urljoin(quotes.xpath('td[3]/a/@href').extract()[0])
			yield scrapy.Request(url, callback = self.parse_dir_content, meta = {"ID": quotes.xpath('td[1]/text()').get()})




	def parse_dir_content(self,response):
		#for quotes in response.xpath('//div[@id="content_right"]'):
			quotes = response.xpath('//div[@id="content_right"]')
			yield{
				'ID':response.meta["ID"],
				'Date of Execution:': quotes.xpath('//p[2]/text()').get(),
				'Inmate:': quotes.xpath('//p[4]/text()').get(),
				'Last Statement:': quotes.xpath('//p[6]/text()').get()
				}

