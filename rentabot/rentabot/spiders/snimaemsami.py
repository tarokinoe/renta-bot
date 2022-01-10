import logging
import os
import scrapy
import json
import telegram
import time

# Telegram bot
BOT_TOKEN = ""
bot = telegram.Bot(token=BOT_TOKEN)
CHAT_ID =
SITE_URL = "https://snimaem-sami.ru"
START_PAGE = SITE_URL + '/objects/?fieldsfilter%5Bobject_type%5D%5B0%5D=802508&fieldsfilter%5Bobject_type%5D%5B1%5D=574&fieldsfilter%5Broom_count_sidebar%5D%5B0%5D=room1&fieldsfilter%5Broom_count_sidebar%5D%5B1%5D=&fieldsfilter%5Broom_count_sidebar%5D%5B2%5D=&fieldsfilter%5Broom_count_sidebar%5D%5B3%5D=&fieldsfilter%5Bprice%5D%5B0%5D=0&fieldsfilter%5Bprice%5D%5B1%5D=505000&fieldsfilter%5Bstation%5D%5B0%5D=921'
PARSING_PERIOD = 100
PARSED_APPARTMENTS_FILE = ''


logger = logging.getLogger(__name__)


class SnimaemsamiSpider(scrapy.Spider):
    name = 'snimaem-sami'
    # allowed_domains = ['snimaem-sami.ru']
    # start_urls = ['https://snimaem-sami.ru/']

    def __init__(self):
        super().__init__()
        with open(PARSED_APPARTMENTS_FILE) as f:
            self._appartments = set(map(str.strip, f))

    def _save_parsed(self, url):
        with open(PARSED_APPARTMENTS_FILE, 'a') as f:
            f.write(url + '\n')

        self._appartments.add(url)

    def start_requests(self):
        yield scrapy.Request(url=START_PAGE, callback=self.parse)

    def parse(self, response, **kwargs):
        snippets = response.xpath('//div[@class="info_object"]')
        for snippet in snippets:
            href = snippet.xpath('./h3/a/@href').get()
            if href and href not in self._appartments:
                # self._save_parsed(href)
                logger.info(f'New appartments: {href}')
                bot.sendMessage(CHAT_ID, SITE_URL + href)
                time.sleep(0.3)

        time.sleep(PARSING_PERIOD)

        yield scrapy.Request(
            url=response.url, callback=self.parse, dont_filter=True
        )
