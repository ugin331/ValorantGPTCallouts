import discord
import credentials

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(name="igl", description="Invite bot to a voice call")
async def igl(ctx: discord.ApplicationContext, channel: discord.VoiceChannel):
    client = await channel.connect()
    audio = discord.FFmpegOpusAudio("audio.wav")
    client.play(audio)
    await ctx.respond("Hey!")


bot.run(credentials.DISCORD_BOT_TOKEN)  # run the bot with the token
