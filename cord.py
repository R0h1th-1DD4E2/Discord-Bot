import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import fetch_url

load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/",intents = intents)

url = fetch_url.search_lofi_music()
print(f"The Link to Video: {url}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def play(ctx):
    if not ctx.author.voice:
        await ctx.send("You are not in a voice channel.")
        return

    voice_channel = ctx.author.voice.channel

    voice_client = None
    
    if not ctx.voice_client:
        ffmpeg_path = r'C:\ffmpeg\bin\ffmpeg.exe'
        voice_client = await voice_channel.connect()
    else:
        voice_client = ctx.voice_client

    voice_client.stop()

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    if url:
        voice_client.play(discord.FFmpegPCMAudio(url, executable=ffmpeg_path, pipe=True, **FFMPEG_OPTIONS))
    else:
        await ctx.send("No valid YouTube URL found.")

@bot.command()
async def pause(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_playing():
        voice_client.pause()
        await ctx.send("Music Paused")

@bot.command()
async def resume(ctx):
    voice_client = ctx.voice_client
    if voice_client.is_paused():
        voice_client.resume()
        await ctx.send("Music resumed")

@bot.command()
async def stop(ctx):
    voice_client = ctx.voice_client
    voice_client.stop()
    await ctx.send("Music Stopped")

bot.run(token)