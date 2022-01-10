import logging
import os
import scrapy
import json
import telegram
import time


logger = logging.getLogger(__name__)


class SnimaemsamiSpider(scrapy.Spider):
    name = 'snimaem-sami'

    def __init__(self):
        super().__init__()
        self._bot = None
        self._appartments = set()

    def _save_parsed(self, url):
        with open(self.settings.get('PARSED_APPARTMENTS_FILE'), 'a') as f:
            f.write(url + '\n')

        self._appartments.add(url)

    def start_requests(self):
        self._bot = telegram.Bot(token=self.settings.get('TELEGRAM_BOT_TOKEN'))

        if not os.path.exists(self.settings.get('PARSED_APPARTMENTS_FILE')):
            with open(self.settings.get('PARSED_APPARTMENTS_FILE'), 'w'):
                pass

        with open(self.settings.get('PARSED_APPARTMENTS_FILE')) as f:
            self._appartments = set(map(str.strip, f))

        url = self.settings.get('SITE_BASE_URL') + self.settings.get('START_PAGE')
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        snippets = response.xpath('//div[@class="info_object"]')
        for snippet in snippets:
            href = snippet.xpath('./h3/a/@href').get()
            if href and href not in self._appartments:
                self._save_parsed(href)
                logger.info(f'New appartments: {href}')
                self._bot.sendMessage(
                    self.settings.get('TELEGRAM_CHAT_ID'),
                    self.settings.get('SITE_BASE_URL') + href
                )
                time.sleep(0.3)

        time.sleep(self.settings.get('PARSING_PERIOD_S'))

        yield scrapy.Request(
            url=response.url, callback=self.parse, dont_filter=True
        )
