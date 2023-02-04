import discord
from discord.ext import commands
from datetime import datetime
import random
import secret
import json
import math

with open("catalog.json", "r") as r:
    catalog = json.load(r)
with open("elevi.json", "r") as r:
    listaElevi = json.load(r)
    

# Env variables --------------------------------------------------------------------------------------------------------
bot = commands.Bot(command_prefix="$", description="This is a Helper Bot", intents=discord.Intents.all())


# Events ---------------------------------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="$comenzi | dynow.tk/bot"))
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
    await ctx.send("⚠Eroare!!!⚠ Esti in vacanta! ᴅᴀɴᴜᴛᴢ ᴍᴏᴅᴇ ON")
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
    embed.add_field(name="Server Region", value=f"{ctx.guild.region}", inline=False)
    embed.add_field(name="Server ID", value=f"{ctx.guild.id}", inline=False)
    embed.set_footer(text="Pentru ajutor contactati: DynoW#9056")
    await ctx.send(embed=embed)
'''


@bot.command()
async def comenzi(ctx):
    await ctx.send("Command is temoraly disabed!")

# Catalog commands -----------------------------------------
@bot.command()
async def top5(ctx):
    mediiElevi = []
    for elev in catalog:
        sumaMedii = 0
        for note in elev["Medii"]:
            sumaMedii = sumaMedii + round(note["Nota"]+0.1)
        average = sumaMedii/len(elev["Medii"])
        mediiElevi.append({"elevID": elev["elevId"], "medie": round(average,2)})
    medieMax1 = {"elevID": "None", "medie": 0}
    medieMax2 = {"elevID": "None", "medie": 0}
    medieMax3 = {"elevID": "None", "medie": 0}
    medieMax4 = {"elevID": "None", "medie": 0}
    medieMax5 = {"elevID": "None", "medie": 0}
    for medie in mediiElevi:
        if medie["medie"] > medieMax1["medie"]:
            medieMax5 = medieMax4
            medieMax4 = medieMax3
            medieMax3 = medieMax2
            medieMax2 = medieMax1
            medieMax1 = medie
        elif medie["medie"] > medieMax2["medie"]:
            medieMax5 = medieMax4
            medieMax4 = medieMax3
            medieMax3 = medieMax2
            medieMax2 = medie
        elif medie["medie"] > medieMax3["medie"]:
            medieMax5 = medieMax4
            medieMax4 = medieMax3
            medieMax3 = medie
        elif medie["medie"] > medieMax4["medie"]:
            medieMax5 = medieMax4
            medieMax4 = medie
        elif medie["medie"] > medieMax5["medie"]:
            medieMax5 = medie
    await ctx.send(f"""{medieMax1} {medieMax2} {medieMax3} {medieMax4} {medieMax5}""")
    
@bot.command()
async def elevi(ctx):
    mesaj = ""
    for elev in listaElevi:
        mesaj = mesaj + elev["$id"] + ". " + elev["nume"] + " - " + elev["elevId"] + "\n"
    await ctx.send(mesaj)
    
@bot.command()
async def medii(ctx):
    mediiElevi = []
    for elev in catalog:
        sumaMedii = 0
        for note in elev["Medii"]:
            sumaMedii = sumaMedii + round(note["Nota"]+0.1)
        average = sumaMedii/len(elev["Medii"])
        mediiElevi.append([elev["elevId"], round(average,2)])
    await ctx.send(mediiElevi)

@bot.command()
async def sync(ctx):
    
    mediiElevi = []
    for elev in catalog:
        sumaMedii = 0
        for note in elev["Medii"]:
            sumaMedii = sumaMedii + round(note["Nota"]+0.1)
        average = sumaMedii/len(elev["Medii"])
        mediiElevi.append([elev["elevId"], round(average,2)])
    await ctx.send(mediiElevi)
    
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
