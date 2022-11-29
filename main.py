import asyncio
from dataclasses import dataclass

import bs4
import httpx
from bs4 import BeautifulSoup
from discord import Colour

from utils.custom_logger import Log
from utils.structs import Product
from utils.webhook import send_webhook

seen = []
log = Log('[MONITOR]')


async def monitor():
    client: httpx.AsyncClient

    urls_to_monitor: list[str] = [
        'https://www.scottycameron.com/store/accessories/',
        'https://www.scottycameron.com/store/apparel/',
        'https://www.scottycameron.com/store/gallery-putters/',
        'https://www.scottycameron.com/store/gallery-creations/'
    ]

    for url in urls_to_monitor:
        async with httpx.AsyncClient() as client:
            try:
                raw_resp: httpx.Response = await client.get(url)
            except Exception:
                log.exception('Error.')
                continue

        resp = BeautifulSoup(raw_resp.text, 'lxml')
        items = resp.select("article[class=product-item]")

        for item in items:
            atc_tag = item.select_one('a[href^="/store/scottyproduct/addtocartplp/"]')
            if atc_tag in seen:
                continue

            if atc_tag.text == 'SOLD' or not atc_tag.text:
                continue

            product = Product(
                name=item.select_one('a[title]').get('title').strip(),
                url='https://www.scottycameron.com' + atc_tag.get('href'),
                price=item.select_one('div[data-test-selector=divPrice]').text.strip(),
                image=item
                    .select_one('img[class*="img-responsive"]')
                    .get('data-src').strip().replace(' ', '')
            )
            print(product.image)
            with open('resp.html', 'w') as file:
                file.write(item.prettify())
            # sleep(300)
            # ping
            await send_webhook(product=product,
                               title='Live Product Detected',
                               color=Colour.teal())
            seen.append(atc_tag)


if __name__ == "__main__":
    from time import sleep
    from datetime import datetime

    while True:
        try:
            asyncio.run(monitor())
        except:
            pass
        sleep(30)
        print(f'[{datetime.now()}]: Checking.')
