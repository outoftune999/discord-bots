import os
import discord

from discord.ext.commands import Bot
from discord.ext import commands
from utility.http_client import HttpClient

class DoggyParty(commands.Cog):

    def __init__(self, bot, httpClient):
        self.bot = bot
        self.httpClient = httpClient

    def run(self, token):
        self.bot.run(token)

    async def get_rando_doggy(self):
        randomDoggyUri = 'https://dog.ceo/api/breeds/image/random'
        response = await self.httpClient.send_api_request(randomDoggyUri)
        return self.get_doggy_url(response)

    async def get_rando_breed(self, breed):
        randomBreedUri = f'https://dog.ceo/api/breed/%s/images/random'
        response = await self.httpClient.send_api_request(randomBreedUri.replace('%s', breed))
        return self.get_doggy_url(response)

    def get_doggy_url(self, responseJson):
        if responseJson['status'] == 'error':
            return None
        return responseJson["message"]

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Ruff ruff!!! {self.bot.user} has connected to Discord!')

    @commands.command()
    async def bark(self, ctx):
        await ctx.channel.send('Woof woof!!!')

    @commands.command()
    async def rando(self, ctx):
        await ctx.channel.send('Hold on, getting a rando good doggy....')
        try:
            url = await self.get_rando_doggy()
            if url == None :
                await ctx.channel.send('I could not find a doggy :(')
            else :
                await ctx.channel.send(url)
        except RuntimeError as ex:
            await handle_exception(ctx, ex)

    @commands.command()
    async def breed(self, ctx, arg):
        await ctx.channel.send(f'Hold on, getting a {arg} doggy....')
        try:
            url = await self.get_rando_breed(arg)
            if url == None :
                await ctx.channel.send('I could not find that doggy :(')
            else :
                await ctx.channel.send(url)
        except RuntimeError as ex:
            await handle_exception(ctx, ex)

    async def handle_exception(self, ctx, ex):
        await ctx.channel.send('Uh oh! There was an issue getting the good doggy!!!')
        print(f'Caught exception while getting random breed: {ex}')

    






    
