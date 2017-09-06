# renta-bot
парсит сайт snimaem-sami.ru и шлет уведомления о новых объявлениях в телеграм

## Настройка
В rentabot/rentabot/spiders/snimaemsami.py нужно указать:  
START_PAGE - страницу с нужным фильтром квартир  
BOT_TOKEN - токен бота  
CHAT_ID - чат, в который бот будет слать уведомления  

## Запуск 
```
cd rentabot
scrapy crawl snimaem-sami
```

## Получить CHAT_ID
Получить СHAT_ID можно как-то при помощи следующих махинаций:
```
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

BOT_TOKEN = ""
bot = telegram.Bot(token=BOT_TOKEN)
updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
```
