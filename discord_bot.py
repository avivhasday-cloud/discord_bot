import discord
from discord.ext import commands
from config import Config
from utils.logger import LOGGER

client = commands.Bot(command_prefix='/')

@client.command()
async def on_ready():
    print('Bot is ready!')


client.load_extension('cogs.music')
client.load_extension('cogs.general')
client.load_extension('cogs.admin')
client.run(Config.TOKEN)
LOGGER.info("Bot is starting now!!!")