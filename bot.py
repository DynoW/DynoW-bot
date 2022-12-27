import discord
from discord.ext import commands
from datetime import datetime
import random
import secret

# Env variables --------------------------------------------------------------------------------------------------------
bot = commands.Bot(command_prefix="$", description="This is a Helper Bot", intents=discord.Intents.default())


# Events ---------------------------------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="$comenzi | dynow.tk"))
    print("Bot is online!")


# Commands -------------------------------------------------------------------------------------------------------------
@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command()
async def zile(ctx, obj: str):
    current_time = datetime.now()
    if obj == "scoala":
        momentspecial = datetime(2023, 6, 15)
        timpramas = momentspecial - current_time
        await ctx.send("Mai sunt ~" + str(timpramas.days) + " zile de scoala.")
    if obj == "bac":
        momentspecial = datetime(2025, 6, 12)
        timpramas = momentspecial - current_time
        await ctx.send("Mai sunt ~" + str(timpramas.days) + " zile pana la bac.")


'''
@bot.command()
async def zile_vacanta(ctx):
    await ctx.send("⚠Eroare!!!⚠ Esti in vacanta!")
    await ctx.channel.send(
        "https://media.cntraveler.com/photos/60e612ae0a709e97d73d9c60/1:1/w_3840,h_3840,c_limit/Beach%20Vacation%20Packing%20List-2021_GettyImages-1030311160.jpg")
'''


@bot.command()
async def random(ctx, randomone: int, randomtwo: int):
    await ctx.send(random.randint(randomone, randomtwo))


# Commands with embends ------------------------------------------------------------------------------------------------
'''@bot.command()
async def serverinfo(ctx):
    embed = discord.Embed(title=f"{ctx.guild.name}", description="Description: "f"{ctx.guild.description}",
                          color=discord.Color.blue())
    embed.add_field(name="Server created at", value=ctx.guild.created_at.strftime("%d.%m.%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Server Owner", value=f"{ctx.guild.owner}", inline=False)
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}", inline=False)
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}", inline=False)
    embed.set_footer(text="Pentru ajutor contactati: DynoW#9056")
    await ctx.send(embed=embed)
'''


@bot.command()
async def comenzi(ctx):
    await ctx.send("Command temoraly disabed!")


# Listening events -----------------------------------------------------------------------------------------------------
@bot.listen()
async def on_message(message):
    if "ntza" in message.content.lower():
        await message.channel.send('Dyno BOT V2.1 Aplha is here!')


@bot.listen()
async def on_message(message):
    if "test" in message.content.lower():
        await message.add_reaction("<💩>")


@bot.listen()
async def on_message(message):
    if "care" in message.content.lower() and message.author.id == 494105470714511360:
        await message.channel.send("pe care")


# Token ----------------------------------------------------------------------------------------------------------------
bot.run(secret.TOKEN)
