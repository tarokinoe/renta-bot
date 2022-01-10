# Renta-bot

## Docker
```
# ../conf/.env
RENTABOT_TELEGRAM_BOT_TOKEN=
RENTABOT_TELEGRAM_CHAT_ID=
RENTABOT_SITE_BASE_URL=https://snimaem-sami.ru
RENTABOT_START_PAGE=
RENTABOT_PARSING_PERIOD_S=100
RENTABOT_PARSED_APPARTMENTS_FILE=/app/parsed.txt
```

```
docker build -t renta-bot .
# dev
docker run --rm --name renta-bot --env-file ../conf/.env.docker renta-bot
# prod
docker run --name renta-bot -d --restart=always --env-file ../conf/.env renta-bot
```