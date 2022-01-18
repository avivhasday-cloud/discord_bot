from youtube_dl import YoutubeDL
import discord
from discord.ext import commands
from discord.utils import get
from utils.player import MusicPlayer
from utils.message_format import  MessageFormater
from utils.logger import LOGGER

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.music_player = MusicPlayer()
        self.message_formatter = MessageFormater()

    @commands.command(name="play", aliases=['p'], help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        voice_channel = ctx.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice is None or not voice.is_connected():
            await voice_channel.connect()
            LOGGER.info(f"Bot is connected to channel {voice_channel}")
            voice = get(self.client.voice_clients, guild=ctx.guild)

        song = self.music_player.search_youtube(query)
        # unpack song
        url, title = song
        if isinstance(song, bool):
            message = f"Could not download song: {title}. Incorrect format try another keyword. This could be due to playlist or a livestream format."
            formated_message = self.message_formatter.get_block_quote_format(message)
            await ctx.send(formated_message)
        else:
            message = f"Song: {title} added to the queue"
            formated_message = self.message_formatter.get_block_quote_format(message)
            await ctx.send(formated_message)
            self.music_player.queue.append(song)
            if not self.music_player.is_playing:
                await self.music_player.play_music(voice)


    @commands.command(name="queue", aliases=['q'], help="Displays the current songs in queue")
    async def show_queue(self, ctx):
        queue_template = "Music Queue\n"
        queue_view = queue_template
        LOGGER.info(f"Queue length: {len(self.music_player.queue)}")
        for i in range(len(self.music_player.queue)):
            _, title = self.music_player.queue[i]
            queue_view += f"{i+1}) {title}\n"

        if queue_view != queue_template:
            formated_message = self.message_formatter.get_italian_code_block_format(queue_view)
            LOGGER.info(f"Queue Function: Sending message to discord channel ")
            await ctx.send(formated_message)
        else:
            message = "No music in queue"
            formated_message = self.message_formatter.get_block_quote_format(message)
            await ctx.send(formated_message)


    @commands.command(name="next", aliases=['n'], help="Skips the current song being played")
    async def skip(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice:
            voice.stop()
            # try to play next in the queue if it exists
            await self.music_player.play_music(voice)

    @commands.command(name="resume", help="Resume music player activity")
    async def resume(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if not voice.is_playing():
            voice.resume()
            message = 'Bot is resuming'
            LOGGER.info(message)
            formated_message = self.message_formatter.get_block_quote_format(message)
            await ctx.send(formated_message)

    # command to pause voice if it is playing
    @commands.command(name="pause", help="Pause music player activity")
    async def pause(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            message = 'Bot has been paused'
            LOGGER.info(message)
            formated_message = self.message_formatter.get_block_quote_format(message)
            await ctx.send(formated_message)

    # command to stop voice
    @commands.command(name="stop", help="Stop music player activity and clear the queue")
    async def stop(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.stop()
            self.music_player.queue.clear()
            message = 'Bot has been stopped'
            LOGGER.info(message)

            formated_message = self.message_formatter.get_block_quote_format(message)
            await ctx.send(formated_message)


def setup(bot):
    bot.add_cog(Music(bot))