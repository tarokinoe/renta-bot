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
