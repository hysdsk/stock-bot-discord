import asyncio
import discord
from configparser import ConfigParser
from .scraper import IndexScraper

configparser = ConfigParser()
configparser.read("config.ini")
config = configparser["DEFAULT"]

token = config["infomation_token"]
announce_channel_id = int(config["channel_id_announce"])
client = discord.Client(intents=discord.Intents.all())

def color_num_for_rate(rate: str):
    if rate.startswith("+"):
        return 31
    if rate.startswith("-"):
        return 34
    return 37

async def send_indicator(channel):
    idxscr = IndexScraper()
    nikkei = idxscr.nikkei225()
    topix = idxscr.topix()
    growth = idxscr.growth250()
    await channel.send(f"""
先物指数
```ansi\n
\u001b[0;37mNikkei225: {nikkei.close.rjust(7)}(\u001b[0;{color_num_for_rate(nikkei.rate)}m{nikkei.rate}\u001b[0;37m)
\u001b[0;37mTopix:     {topix.close.rjust(7)}(\u001b[0;{color_num_for_rate(topix.rate)}m{topix.rate}\u001b[0;37m)
\u001b[0;37mGrowth250: {growth.close.rjust(7)}(\u001b[0;{color_num_for_rate(growth.rate)}m{growth.rate}\u001b[0;37m)```
""")

@client.event
async def on_ready():
    channel = client.get_channel(announce_channel_id)
    if channel:
        await send_indicator(channel)
    await client.close()

async def main():
    await client.start(token)

if __name__ == "__main__":
    asyncio.run(main())
