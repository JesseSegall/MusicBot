from logger_config import setup_logger
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import yt_dlp

logger = setup_logger()

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
PATH = os.getenv('FFMPEG_PATH')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')


@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f'Joined {channel}')
    else:
        await ctx.send("You're not connected to a voice channel")


@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            logger.info("FFMPEG process should be stopped here.")
        await ctx.voice_client.disconnect()
        await ctx.send('Left voice channel')
    else:
        await ctx.send("Not in a voice channel")


@bot.command()
async def play(ctx, *, song_name):
    logger.info(f'Received play command for song: {song_name}')

    try:

        if not ctx.author.voice:
            await ctx.send("You need to be in a voice channel first so the bot knows where to go.")
            logger.warning(f"User {ctx.author} tried to play music without being in a voice channel")
            return

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(f'ytsearch:{song_name}', download=False)['entries'][0]
                url = info['url']
            except IndexError:
                await ctx.send(f"Couldn't find any song matching '{song_name}'. Please try a different search term.")
                logger.warning(f"No song found for search term: {song_name}")
                return
            except Exception as e:
                await ctx.send(f"An error occurred while searching for the song: {str(e)}")
                logger.error(f"Error searching for song '{song_name}': {str(e)}", exc_info=True)
                return

        if not ctx.voice_client:
            try:
                await ctx.author.voice.channel.connect()
            except Exception as e:
                await ctx.send(f"Couldn't connect to the voice channel: {str(e)}")
                logger.error(f"Error connecting to voice channel: {str(e)}", exc_info=True)
                return

        try:
            ctx.voice_client.play(discord.FFmpegPCMAudio(url, executable=PATH))
            await ctx.send(f"Now playing: {info['title']}")
            logger.info(f"Now playing: {info['title']}")
        except Exception as e:
            await ctx.send(f"An error occurred while trying to play the song: {str(e)}")
            logger.error(f"Error playing song '{song_name}': {str(e)}", exc_info=True)

    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {str(e)}")
        logger.error(f"Unexpected error in play command: {str(e)}", exc_info=True)


bot.run(TOKEN)
