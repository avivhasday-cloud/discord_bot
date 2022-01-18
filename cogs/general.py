import discord
from discord.ext import commands
import os

ADMIN_USER = os.environ.get('ADMIN_USER')

class General(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel!")
        voice_channel = ctx.author.voice.channel
        print(voice_channel)
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command(name='disconnect',aliases=['bye'])
    async def disconnect(self, ctx):
        await ctx.send("I'm leaving the channel, Bye :)")
        await ctx.voice_client.disconnect()
    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! \nlatency: {round(self.client.latency * 1000)}ms')

    @commands.command(aliases=['name'])
    async def say_name(self, ctx):
        await ctx.send(f'Your name is {ctx.author.name}')


    @commands.command(aliases=['commandlist', 'commands'])
    async def _help(self, ctx):
        await ctx.send_help()


def setup(bot):
    bot.add_cog(General(bot))