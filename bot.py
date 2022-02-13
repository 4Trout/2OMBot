import config
import random
import asyncio
from discord import Game
from discord.ext.commands import Bot
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

BOT_PREFIX = ("?", "!")
client = Bot(command_prefix=BOT_PREFIX)

@client.command()
async def twomb(ctx):
    await twoPrice('2omb')

@client.command()
async def thromb(ctx):
    await threePrice('2omb')

async def twoPrice(name):
    json = cg.get_price(ids=['2share', '2omb-finance', 'fantom'], vs_currencies='usd')
    print(json)
    #await client.say("{} coin price is: ${}".format(name, value))

async def threePrice(name):
    json = cg.get_price(ids=['30mb-token', '3shares', 'fantom'], vs_currencies='usd')
    print(json)
    #await client.say("{} coin price is: ${}".format(name, value))

async def getData(coin):
    if coin == '3omb' or coin == '2omb':
        getPeg()

async def getPeg(price, ftm):
    return

async def updateStatus(title, val):
    label = title + ': ' + val
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=label))

client.run(config.secret)
