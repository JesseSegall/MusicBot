from sys import exc_info
import asyncio
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
# Dictionary that has the key being unique guild ID and the value being another dictionary
# that holds title and requester.
current_songs = {}
logger.info(f'Current Songs: {current_songs}')

bot = commands.Bot(command_prefix='$', intents=intents)
ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0',  # Bind to IPv4
}


@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user}')
    await asyncio.sleep(1)
    for guild in bot.guilds:
        print(f'Connected to guild: {guild.name}')
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send("Hello! Type $commands to see all current commands.")
                break


@bot.command()
async def commands(ctx):
    await ctx.send('''Bot Commands:
    $join causes the bot to join the voice channel you are currently in.
    $play {song name} to play a song.
    $pause to pause the current song.
    $stop to stop playing the current song.
    $resume to resume playing the paused song.
    $quit to remove the bot from the current voice channel.''')


@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f'Joined {channel}')
    else:
        await ctx.send("You're not connected to a voice channel")


@bot.command(name='quit')
async def quit_command(ctx):
    if ctx.voice_client:
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            logger.info("FFMPEG process should be stopped here.")
        await ctx.voice_client.disconnect()
        await ctx.send('Left voice channel')
    else:
        await ctx.send("Not in a voice channel")


@bot.command()
async def song(ctx):
    current_song = current_songs.get(ctx.guild.id)
    if current_song:
        title = current_song['title']
        requester = current_song['requester']
        await ctx.send(f'The current song is: {title} and it was chosen by: {requester}.')
    else:
        await ctx.send("There is no song currently playing.")


@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        current_song = current_songs.pop(ctx.guild.id, None)
        song_title = current_song['title'] if current_song else 'Unknown'
        await ctx.send(f'Stopped playing {song_title}')
        logger.info(f'Stopped playing: {song_title}')
    else:
        await ctx.send("No song is currently playing.")


@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Paused the current song.")
        logger.info('Song paused')
    else:
        await ctx.send("No song is currently playing.")


@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Resumed the song.")
        logger.info('Song resumed')
    else:
        await ctx.send("No song is currently paused.")


@bot.command()
async def play(ctx, *, song_name):
    logger.info(f'Received play command for song: {song_name}')

    if not ctx.author.voice:
        await ctx.send("You need to be in a voice channel first so the bot knows where to go.")
        logger.warning(f"User {ctx.author} tried to play music without being in a voice channel")
        return

    if not ctx.voice_client:
        try:
            await ctx.author.voice.channel.connect()
            await ctx.send(f'Joined {ctx.author.voice.channel}')
        except Exception as e:
            await ctx.send(f"Couldn't connect to the voice channel: {str(e)}")
            logger.error(f"Error connecting to voice channel: {str(e)}", exc_info=True)
            return

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(song_name, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            url = info['url']
            title = info.get('title', 'Unknown Title')
        except Exception as e:
            await ctx.send(f"An error occurred while searching for the song: {str(e)}")
            logger.error(f"Error searching for song '{song_name}': {str(e)}", exc_info=True)
            return

    try:
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -loglevel quiet',
            'options': '-vn'
        }

        source =  discord.FFmpegOpusAudio(
            url,
            executable=PATH,
            **ffmpeg_options
        )
        ctx.voice_client.play(source)
        await ctx.send(f"Now playing: {title}")
        logger.info(f"Now playing: {title}")
        guild_id = ctx.guild.id
        current_songs[guild_id] = {
            'title': title,
            'requester': ctx.author.name,
        }
    except Exception as e:
        await ctx.send(f"An error occurred while trying to play the song: {str(e)}")
        logger.error(f"Error playing song '{song_name}': {str(e)}", exc_info=True)



bot.run(TOKEN)
