from youtube_dl import YoutubeDL
import discord
from discord import ClientException
from utils.music_queue import MusicQueue
from utils.logger import LOGGER


class MusicPlayer():

    def __init__(self):
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True', 'verbose': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}
        self.music_queue = MusicQueue()
        self.is_playing = False

    # searching the item on youtube
    def search_youtube(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                LOGGER.info(f"Searching {item} in youtube")
                if item.startswith("http"):
                    LOGGER.info(f"{item} is URL")
                    info = ydl.extract_info(item, download=False)
                else:
                    LOGGER.info(f"{item} is search query")
                    info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False

        return info['formats'][0]['url'], info['title']

    def play_next(self, voice):
        if len(self.music_queue) > 0:
            self.is_playing = True
            # get the first url
            (url, title) = self.music_queue.queue[0]
            # remove the first element as you are currently playing it
            self.music_queue.pop(0)
            LOGGER.info(f"Start playing {title}")
            source = discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS)
            voice.play(source, after=lambda e: self.play_next(voice))
        else:
            self.is_playing = False

    # infinite loop checking
    async def play_music(self, voice):
        if len(self.music_queue) > 0:
            try:
                self.is_playing = True
                (url, title) = self.music_queue.queue[0]
                # remove the first element as you are currently playing it
                self.music_queue.pop(0)
                LOGGER.info(f"Start playing {title}")
                voice.play(discord.FFmpegPCMAudio(url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next(voice))
            except ClientException as err:
                print(err)
        else:
            self.is_playing = False

