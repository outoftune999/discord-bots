import os
import discord
import aiohttp
import json

from discord.ext.commands import Bot
from discord.ext import commands
from pathlib import Path
from dotenv import load_dotenv
from aiohttp import web

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

bot = commands.Bot(command_prefix = 'dp-')

async def send_api_request(uri):
    async with aiohttp.ClientSession() as session:
        async with session.get(uri) as response:
            if response.status != 200 :
                print(f'Received non-200 status {response.status}')
            responseBody = await response.text()
            responseJson = json.loads(responseBody)
            return responseJson

def get_doggy_url(responseJson):
    if responseJson['status'] == 'error':
        return None
    return responseJson["message"]

async def get_rando_doggy():
    random_doggy_uri = 'https://dog.ceo/api/breeds/image/random'
    response = await send_api_request(random_doggy_uri)
    return get_doggy_url(response)

async def get_rando_breed(breed):
    random_breed_uri = f'https://dog.ceo/api/breed/{breed}/images/random'
    response = await send_api_request(random_breed_uri)
    return get_doggy_url(response)

async def handle_exception(ctx, ex):
    await ctx.channel.send('Uh oh! There was an issue getting the good doggy!!!')
    print(f'Caught exception while getting random breed: {ex}')

@bot.event
async def on_ready():
    print(f'Ruff ruff!!! {bot.user} has connected to Discord!')

@bot.event
async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(
             f'Ruff!!! Ruff!!! Ruff!!! {member.name}, welcome to the Discord server!'
        )

@bot.command(pass_context=True)
async def bark(ctx):
    await ctx.channel.send('Woof woof!!!')

@bot.command(pass_context=True)
async def rando(ctx):
    await ctx.channel.send('Hold on, getting a rando good doggy....')
    try:
        url = await get_rando_doggy()
        if url == None :
            await ctx.channel.send('I could not find a doggy :(')
        else :
            await ctx.channel.send(url)
    except RuntimeError as ex:
        await handle_exception(ctx, ex)

@bot.command(pass_context=True)
async def breed(ctx, arg):
    await ctx.channel.send(f'Hold on, getting a {arg} doggy....')
    try:
        url = await get_rando_breed(arg)
        if url == None :
            await ctx.channel.send('I could not find that doggy :(')
        else :
            await ctx.channel.send(url)
    except RuntimeError as ex:
        await handle_exception(ctx, ex)
    
bot.run(TOKEN)