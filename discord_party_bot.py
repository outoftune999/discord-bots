import os
from doggy_party.doggy_party import DoggyParty
from comrade_jeb.comrade_jeb import ComradeJeb
from discord.ext import commands
from multiprocessing import Process
from utility.http_client import HttpClient

TOKEN = os.getenv('DISCORD_TOKEN')
doggyPartyBot = commands.Bot(command_prefix = 'dp-')
comradeJebBot = commands.Bot(command_prefix = 'jeb-')

httpClient = HttpClient()
doggyParty = DoggyParty(doggyPartyBot, httpClient)
doggyPartyBot.add_cog(doggyParty)
comradeJeb = ComradeJeb(comradeJebBot)
comradeJebBot.add_cog(comradeJeb)

def runDoggyParty():
    doggyParty.run(TOKEN)

def runComradeJeb():
    comradeJeb.run(TOKEN)

p = Process(target=runDoggyParty)
p.start()

p = Process(target=runComradeJeb)
p.start()


