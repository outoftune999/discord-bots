import os
import discord
import aiohttp
import json

from discord.ext.commands import Bot
from discord.ext import commands
from pathlib import Path
from dotenv import load_dotenv
from aiohttp import web

class ComradeJeb(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def run(self, token):
        self.bot.run(token)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'PLEASE CLAP!!! {self.bot.user} has connected to Discord!')

    @commands.command()
    async def please_clap(self, ctx):
        await ctx.channel.send('PLEASE CLAP!!!')

    