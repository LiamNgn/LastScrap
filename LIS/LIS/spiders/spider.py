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
			"Last Name": info.xpath('td[4]/text()').get(),
			"First Name": info.xpath('td[5]/text()').get(),
			"TDCJ number": info.xpath('td[6]/text()').get(),
			"Age": info.xpath('td[7]/text()').get(),
			"Date of Execution": info.xpath('td[8]/text()').get(),
			"Race": info.xpath('td[9]/text()').get(),
			"County": info.xpath('td[10]/text()').get(),
			}
		for quotes in response.xpath('//td//a[contains(@href,"last.html")]/@href'):
			url = response.urljoin(quotes.extract())
			yield scrapy.Request(url, callback = self.parse_dir_content)

	def parse_dir_content(self,response):
		for quotes in response.xpath('//div[@id="content_right"]'):
			yield{
				'Date of Execution:': quotes.xpath('//p[2]').get(),
				'Inmate:': quotes.xpath('//p[4]').get(),
				'Last Statement:': quotes.xpath('//p[6]').get()
				}

