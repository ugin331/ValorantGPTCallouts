import asyncio
import discord
import credentials
from .image import *
from .gpt import GPTClient
from .screen_mac import ScreenshotClient


bot = discord.Bot()
screenshotter = ScreenshotClient()
gpt = GPTClient()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="igl", description="Invite bot to a voice call")
async def igl(ctx: discord.ApplicationContext, channel: discord.VoiceChannel):
    old_vc = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if old_vc:
        old_vc.cleanup()

    client = await channel.connect(reconnect=True)
    await ctx.respond("Joined!")
    await ask_gpt(client)


async def ask_gpt(client: discord.VoiceClient):
    while client.is_connected():
        capture = screenshotter.mss_capture()
        im = sct_to_PIL(capture)
        save_PIL_to_disk(im)
        b64 = b64_encode(im)
        im.close()
        print('image captured')

        gpt_response = gpt.prompt(b64)
        if not gpt_response.is_valorant:
            await asyncio.sleep(5)
            continue

        gpt.audio_prompt(gpt_response.instructions)

        audio = discord.FFmpegOpusAudio("audio.wav")
        print(client.is_playing())
        await client.play(audio, wait_finish=True)
        print('audio played')
        audio.cleanup()
        await asyncio.sleep(20)
        print('sleep finished')
    print('bot disconnected')


def run():
    bot.run(credentials.DISCORD_BOT_TOKEN)  # run the bot with the token
