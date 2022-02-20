import config
import random
import asyncio
import discord
from discord import Game
from discord import Color
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import CommandNotFound
from discord.utils import get

# Coingecko setup
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

# MySQL setup
from mysql.connector import (connection)
cnx = connection.MySQLConnection(user=config.dbuser,password=config.dbpass,host=config.dbhost,database=config.db)
cursor = cnx.cursor()

# Global bot config
BOT_PREFIX = ("?")
client = Bot(command_prefix=BOT_PREFIX)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRole):
        em = discord.Embed(title=f"Permission Error", description=f"You don't have permission to use this command!", color=Color.red())
        await ctx.send(embed=em)
        return
    raise error

# Bot commands
@client.command()
@commands.has_role(config.supportRole)
async def verify(ctx, user: discord.Member, wallet, role:discord.Role=None):
    res = await dbWalletCheck(wallet)

    if res:
        em = discord.Embed(title=f"Error: Already Registered!", description=f"Wallet already exists for user: <@" + res[0] + ">", color=Color.red())
        await ctx.send(embed=em)
    else:
        await dbAdd(wallet, user.id)
        if role is None:
            em = discord.Embed(title=f"Verification Success!", description=f"Wallet has been verified, please grant user appropriate role!", color=Color.blue())
            await ctx.send(embed=em)
        else:
            await user.add_roles(role)
            role_get = get(user.guild.roles, name="Pending Verification")
            await user.remove_roles(role_get)
            em = discord.Embed(title=f"Verification Success!", description=f"Wallet has been verified and role has been automatically granted!", color=Color.green())
            await ctx.send(embed=em)


@client.command()
@commands.has_role(config.supportRole)
async def add(ctx, user: discord.Member, wallet, role: discord.Role=None):
    await dbAdd(wallet, user.id)
    if role is None:
        em = discord.Embed(title=f"Verification Success!", description=f"Wallet has been verified, please grant user appropriate role if necessary!", color=Color.blue())
        await ctx.send(embed=em)
    else:
        await user.add_roles(role)
        role_get = get(user.guild.roles, name="Pending Verification")
        await user.remove_roles(role_get)
        em = discord.Embed(title=f"Verification Success!", description=f"Wallet has been verified and role has been automatically granted!", color=Color.green())
        await ctx.send(embed=em)

@client.command()
@commands.has_role(config.supportRole)
async def check(ctx, addr):
    res = await dbWalletCheck(addr)

    if res:
        em = discord.Embed(title=f"Already Registered!", description=f"Wallet already exists for user: <@" + res[0] + ">", color=Color.blue())
        await ctx.send(embed=em)
    else:
        em = discord.Embed(title=f"Not Registered!", description=f"Wallet is not yet registered!", color=Color.blue())
        await ctx.send(embed=em)

@client.command()
@commands.has_role(config.supportRole)
async def lookup(ctx, user: discord.Member):
    res = await dbUserCheck(user.id)

    if res:
        em = discord.Embed(title=f"Wallet Found!", description=f"User wallet is: " + res[0], color=Color.blue())
        await ctx.send(embed=em)
    else:
        em = discord.Embed(title=f"Not Registered!", description=f"User has no wallet registered!", color=Color.blue())
        await ctx.send(embed=em)

@client.command()
@commands.has_role(config.supportRole)
async def remove(ctx, wallet):
    await dbRemove(wallet)
    em = discord.Embed(title=f"Wallet Removed!", description=f"Wallet was removed from verification system!", color=Color.blue())
    await ctx.send(embed=em)


# @client.command()
# async def twomb(ctx):
#     await twoPrice('2omb')
#
# @client.command()
# async def thromb(ctx):
#     await threePrice('2omb')

# FUNCTIONS

async def dbWalletCheck(addr):
    checkQuery = 'SELECT discId FROM wallets WHERE address = %s'
    checkData = (addr,)

    cursor.execute(checkQuery, checkData)
    if cursor.rowcount > 0:
        return False
    else:
        return cursor.fetchone()

async def dbUserCheck(discId):
    checkQuery = 'SELECT address FROM wallets WHERE discId = %s'
    checkData = (discId,)

    cursor.execute(checkQuery, checkData)
    if cursor.rowcount > 0:
        return False
    else:
        return cursor.fetchone()

async def dbAdd(addr, discId):
    addQuery = 'REPLACE INTO wallets (address, discId) VALUES (%s, %s)'
    addData = (addr, discId)

    cursor.execute(addQuery, addData)
    cnx.commit()
    return

async def dbRemove(addr):
    removeQuery = 'DELETE FROM wallets WHERE address = %s'
    removeData = (addr,)

    cursor.execute(removeQuery, removeData)
    cnx.commit()
    return

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
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=label))

client.run(config.secret)
