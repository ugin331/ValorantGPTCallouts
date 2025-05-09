import discord
import credentials
import time
from .image import sct_to_PIL, save_PIL_to_disk, b64_encode
from .gpt import GPTClient

try:
    from src.screen import ScreenshotClient
except ImportError:
    from src.screen_mac import ScreenshotClient

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="igl", description="Invite bot to a voice call")
async def igl(ctx: discord.ApplicationContext, channel: discord.VoiceChannel):
    client = await channel.connect()
    screenshotter = ScreenshotClient()
    gpt = GPTClient()
    await ctx.respond("Joined!")

    while client.is_connected():
        capture = screenshotter.mss_capture()
        im = sct_to_PIL(capture)
        save_PIL_to_disk(im)
        b64 = b64_encode(im)

        gpt_response = gpt.prompt(b64)
        print(gpt_response)

        gpt.audio_prompt(gpt_response)

        audio = discord.FFmpegOpusAudio("audio.wav")
        await client.play(audio, wait_finish=True)
        time.sleep(15)

    screenshotter.cleanup()


def run():
    bot.run(credentials.DISCORD_BOT_TOKEN)  # run the bot with the token
