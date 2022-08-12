from youtube_dl import YoutubeDL
import discord
from discord.ext import commands
from discord.utils import get
from utils.player import MusicPlayer
from utils.message_format import MessageFormater
from utils.logger import LOGGER


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.music_player = MusicPlayer()
        self.message_formatter = MessageFormater()

    @commands.command(name="play", aliases=['p'], help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)
        song_list_requests = query.split(",") if ',' in query else [query]
        voice_channel = ctx.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice is None or not voice.is_connected():
            await voice_channel.connect()
            if len(self.music_player.music_queue) > 0:
                self.music_player.music_queue.clear()
                LOGGER.info(f"Music player queue is not empty, clearing queue now!")
            LOGGER.info(f"Bot is connected to channel {voice_channel}")
            voice = get(self.client.voice_clients, guild=ctx.guild)

        songs = [self.music_player.search_youtube(query) for query in song_list_requests]
        # unpack song
        for song in songs:
            if isinstance(song, bool):
                message = f"Could not download song: {query}. Incorrect format try another keyword. This could be due to playlist or a livestream format."
                formated_message = self.message_formatter.get_block_quote_format(message)
                await ctx.send(formated_message)
            else:
                url, title = song
                message = f"Song: {title} added to the queue"
                formated_message = self.message_formatter.get_block_quote_format(message)
                await ctx.send(formated_message)
                self.music_player.music_queue.put(song)
        if not self.music_player.is_playing:
            await self.music_player.play_music(voice)

    @commands.command(name="queue", aliases=['q'], help="Displays the current songs in queue")
    async def show_queue(self, ctx):
        queue_template = "Music Queue\n"
        queue_view = queue_template
        queue = self.music_player.music_queue.queue
        LOGGER.info(f"Queue length: {len(queue)}")
        for i in range(len(queue)):
            _, title = queue[i]
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
            item = self.music_player.music_queue.get()
            if item is None:
                message = f"There is no songs in music queue"
            else:
                message = f"Skipping to song: {item[1]}"
            formated_message = self.message_formatter.get_block_quote_format(message)
            await ctx.send(formated_message)
            if item is not None:
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
            self.music_player.music_queue.clear()
            message = 'Bot has been stopped'
            LOGGER.info(message)

            formated_message = self.message_formatter.get_block_quote_format(message)
            await ctx.send(formated_message)

    # command to loop queue
    @commands.command(name="loop", help="loop music queue")
    async def loop(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing() and self.music_player.music_queue:
            message = 'Looping over Music Queue'
            LOGGER.info(message)
            self.music_player.music_queue.set_loop_over_queue(True)
            formated_message = self.message_formatter.get_block_quote_format(message)
            await ctx.send(formated_message)

    # command to unloop queue
    @commands.command(name="unloop", help="unloop music queue")
    async def unloop(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing() and self.music_player.music_queue:
            message = 'Stopping loop over Music Queue'
            LOGGER.info(message)
            self.music_player.music_queue.set_loop_over_queue(False)
            formated_message = self.message_formatter.get_block_quote_format(message)
            await ctx.send(formated_message)

def setup(bot):
    bot.add_cog(Music(bot))