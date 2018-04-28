import os
import platform
import discord
from discord.ext import commands

# Setup Token File Input
path = os.path.realpath('')
operating_system = platform.platform()
all_contents = ''
if "Windows" in operating_system:
    f = open(path + '\\token.txt','r')
    all_contents = f.read()
else:
    f = open(path + '/token.txt','r')
    all_contents = f.read()

# FOR DISCORD
bot = commands.Bot(command_prefix='&', description='')

@bot.event
async def on_ready():
   print("Running version number: " + discord.__version__)
   print("Logged in as:", bot.user.name, bot.user.id)

bot.run(all_contents[:len(all_contents)-1])
