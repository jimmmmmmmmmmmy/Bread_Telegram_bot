
import requests
import asyncio
from telegram import Bot
from price_scraper import ndx_price

def get_ndx():
    return ndx_price()

# get JSON
def get_json_data(url):
    response = requests.get(url)
    return response.json()

# format JSON into text
def format_message(data, price: float):
    if data['qty'] == 0.0:
        return f"Flat\n{get_ndx()} \nResult: {price} points"
    elif data['qty'] > 0.0:
        return f"Long {data['symbol']} {get_ndx()}"
    elif data['qty'] < -0.0:
        return f"Short {data['symbol']} {get_ndx()}"
    else:
        return f"Symbol: {data['symbol']}\nQuantity: {data['qty']}"


# send message to telegram
async def send_to_telegram(bot_token, channel_id, message):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=channel_id, text=message)


# run bot
async def main():
    BOT_TOKEN = 'BOT TOKEN : BOT TOKEN'
    CHANNEL_ID = ' CHANNEL ID '
    JSON_URL = ' BREAD CAPITAL POSITIONS URL '

    previous_qty = None
    previous_price = 0.00

    while True:
        try:
            json_data = get_json_data(JSON_URL)
            if json_data is None:
                await asyncio.sleep(60)
                continue

            current_qty = json_data['qty']
            ndx_price = float(get_ndx().replace(",", ""))

            if current_qty != previous_qty:
                trade_result = ndx_price - previous_price
                formatted_message = format_message(json_data, trade_result)
                await send_to_telegram(BOT_TOKEN, CHANNEL_ID, formatted_message)
                previous_qty = current_qty
                previous_price = ndx_price

            await asyncio.sleep(60)
        except Exception as error:
            print(f"An error occurred: {error}")
            await asyncio.sleep(60)

asyncio.run(main())
