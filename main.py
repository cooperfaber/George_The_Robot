import discord
from discord.ext import commands
from discord.ext import tasks
import random
import time

random.seed(a=None, version=2)

class GeorgeBot(discord.Client):
    GeorgeBot = discord.Client()
    #commands are moses, because of the 10 commdandments
    #no? biblical references aren't classy any more?
    moses = commands.Bot(command_prefix = '/')


client = GeorgeBot()
client.run('ODcxMTA2MzAxMTkzNzc3MTgy.YQWe9g.IWTjCCiMxw5T14Xbakyv0kiErwI')