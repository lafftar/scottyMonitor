import asyncio
from asyncio import sleep

import aiohttp
from discord import Colour, Embed, Webhook

from utils.custom_logger import logger
from utils.structs import Product


async def send_webhook(product: Product, title: str = '',  webhook_url: str = None, color: Colour = None,
                       title_link='https://discord.com'):
    if not color:
        color = Colour.dark_red()
    if not webhook_url:
        webhook_url = 'https://discord.com/api/webhooks/1043623209574072441/' \
                      'qKhxv70kGZnWxgSly6MPk3Ekj-pG7FAWXWvuaBH-saZ_MmFFsV3sweOwBKpuvvvtjsJf'

    # create embed
    embed = Embed(title=title, color=color, url=title_link)
    embed.set_footer(text='WINX4 Bots - winwinwinwin#0001',
                     icon_url='https://images6.alphacoders.com/909/thumb-1920-909641.png')

    embed.add_field(name=f'[{product.price}] {product.name} - ATC:', value=f'{product.url}', inline=False)
    embed.set_thumbnail(url=product.image)

    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as webhook_client:
            webhook = Webhook.from_url(url=webhook_url, session=webhook_client)
            await webhook.send(username='HCBP',
                               avatar_url=
                               'https://i.pinimg.com/originals/2f/08/ab/2f08ab311cb92ed2cfafc691b12a8ce2.jpg',
                               embed=embed,
                               )
    except Exception:
        logger().exception(f'Webhook Failed - {product.image}')
        await sleep(2)


if __name__ == "__main__":
    async def run():
        client = aiohttp.ClientSession()
        try:
            # send webhook
            embed_dict = {
                'Email': f'||test||',
                'IP': f'||test.te.tes.tes||'
            }
            await send_webhook(embed_dict=embed_dict,
                               title='Account Created',
                               color=Colour.teal())
        finally:
            await client.close()


    asyncio.run(run())
