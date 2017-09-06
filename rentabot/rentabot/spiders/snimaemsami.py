import os
import scrapy
import json
import telegram
import time

# Telegram bot
BOT_TOKEN = ""
bot = telegram.Bot(token=BOT_TOKEN)
CHAT_ID = None

# 
PARSED_APPARTMENTS = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  'parsed_appartments.txt')

SITE_URL = "http://snimaem-sami.ru"
START_PAGE = SITE_URL + '/objects/?fieldsfilter%5Bobject_type%5D%5B%5D=802508&fieldsfilter%5Bobject_type%5D%5B%5D=574&fieldsfilter%5Broom_count_sidebar%5D%5B%5D=room1&fieldsfilter%5Broom_count_sidebar%5D%5B%5D=&fieldsfilter%5Broom_count_sidebar%5D%5B%5D=&fieldsfilter%5Broom_count_sidebar%5D%5B%5D=&fieldsfilter%5Bstation%5D%5B%5D=667&fieldsfilter%5Bstation%5D%5B%5D=831&fieldsfilter%5Bstation%5D%5B%5D=663&fieldsfilter%5Bstation%5D%5B%5D=691&fieldsfilter%5Bstation%5D%5B%5D=665&fieldsfilter%5Bstation%5D%5B%5D=671&fieldsfilter%5Bstation%5D%5B%5D=925&fieldsfilter%5Bstation%5D%5B%5D=808&fieldsfilter%5Bstation%5D%5B%5D=806&fieldsfilter%5Bstation%5D%5B%5D=882&fieldsfilter%5Bstation%5D%5B%5D=901&fieldsfilter%5Bstation%5D%5B%5D=618&fieldsfilter%5Bstation%5D%5B%5D=614&fieldsfilter%5Bprice%5D%5B0%5D=0&fieldsfilter%5Bprice%5D%5B1%5D=22000'
PARSING_PERIOD = 100


appartments = set()


class SnimaemSami(scrapy.Spider):
    name = "snimaem-sami"

    def start_requests(self):
        with open(PARSED_APPARTMENTS) as f:
            for line in f:
                appartments.add(line.strip())

        yield scrapy.Request(url=START_PAGE, callback=self.parse)

    def parse(self, response):
        objects = response.css(".middle .inlist_object")
        for obj in objects:
            href = obj.css(".further_object > a::attr(href)").extract_first()
            if href not in appartments:
                with open(PARSED_APPARTMENTS, 'a') as f:
                    f.write(href + '\n')
                appartments.add(href)
                bot.sendMessage(CHAT_ID, SITE_URL + href)
                time.sleep(0.3)
        
        time.sleep(PARSING_PERIOD)

        yield scrapy.Request(url=response.url, callback=self.parse, dont_filter=True)
