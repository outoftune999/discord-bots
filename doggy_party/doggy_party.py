import os
import discord
import io

from discord.ext.commands import Bot
from discord.ext import commands
from utility.http_client import HttpClient
from discord import File

class DoggyParty(commands.Cog):

    def __init__(self, bot, httpClient):
        self.bot = bot
        self.httpClient = httpClient

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
    
    @commands.command()
    async def fetch(self, ctx, arg):
        items = []
        if arg == 'breeds' :
            items = await self.get_breed_list()
        else :
            await ctx.channel.send('Ruff!!! Ruff!!! I couldnt find that! *licks crotch*')
        await self.send_list(items, ctx)
    
    def run(self, token):
        self.bot.run(token)

    async def send_list(self, li, ctx):
        listStr = self.turn_list_into_string(li)
        await ctx.channel.send(listStr)

    def turn_list_into_string(self, li):
        listStr = ''
        for item in li:
            listStr += item + ", "
        return listStr

    async def handle_exception(self, ctx, ex):
        await ctx.channel.send('Uh oh! There was an issue getting the good doggy!!!')
        print(f'Caught exception while getting random breed: {ex}')

    async def get_rando_doggy(self):
        randomDoggyUri = 'https://dog.ceo/api/breeds/image/random'
        response = await self.httpClient.send_api_request(randomDoggyUri)
        return self.get_doggy_url(response)

    async def get_rando_breed(self, breed):
        randomBreedUri = f'https://dog.ceo/api/breed/%s/images/random'
        response = await self.httpClient.send_api_request(randomBreedUri.replace('%s', breed.lower()))
        return self.get_doggy_url(response)
    
    async def get_breed_list(self):
        breedListUri = 'https://dog.ceo/api/breeds/list/all'
        response = await self.httpClient.send_api_request(breedListUri)
        return self.extract_breed_list(response)

    def get_doggy_url(self, responseJson):
        if responseJson['status'] == 'error':
            return None
        return responseJson["message"]
    
    def extract_breed_list(self, responseJson):
        breeds = []
        message = responseJson["message"]
        for key in message.keys():
            breeds.append(key)
        return breeds


    






    
