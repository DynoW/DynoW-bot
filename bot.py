import discord
from discord.ext import commands
from datetime import datetime
import secret
import pymongo
# import json
# import os

myclient = pymongo.MongoClient("mongodb+srv://dynow:Naff1324@cluster0.lk2h7ri.mongodb.net/?retryWrites=true&w=majority")
db =  myclient["db-catalog"]
catalog = db["catalog"]
listaElevi = db["elevi"]

# Env variables --------------------------------------------------------------------------------------------------------
bot = commands.Bot(command_prefix="$", description="This is a Helper Bot", intents=discord.Intents.all())

# Events ---------------------------------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="$comenzi | dynow.tk/bot"))
    print("Bot is online!")

# Functions ------------------------------------------------------------------------------------------------------------
def calcMedii():
    global mediiElevi
    mediiElevi = []
    for elev in catalog.find():
        sumaMedii = 0
        for medie in elev["Medii"]:
            sumaMedii = sumaMedii + round(medie["Nota"]+0.1)
        averageMedii = (sumaMedii+10)/(len(elev["Medii"])+1)
        mediiElevi.append({"elevId": elev["elevId"], "medie": round(averageMedii,2)})
calcMedii()

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


# Commands with embends ------------------------------------------------------------------------------------------------
@bot.command()
async def comenzi(ctx):
    await ctx.send("Command is temoraly disabed!")

# Catalog commands -----------------------------------------------------------------------------------------------------
@bot.command()
async def elevi(ctx):
    mesaj = ""
    for elev in listaElevi.find():
        if elev["elevId"]!="":
            mesaj = mesaj + f"""{elev["$id"]}. {elev["nume"]} - `{elev["elevId"]}`\n"""
        else:
            mesaj = mesaj + f"""{elev["$id"]}. {elev["nume"]} - \n"""
    await ctx.send(mesaj)


@bot.command()
async def all(ctx):
    mesaj = ""
    for medii in mediiElevi:
        v=0
        for elev in listaElevi.find():
            if elev["elevId"]==medii["elevId"]:
                mesaj = mesaj + f"""`{medii["elevId"]}` - {medii["medie"]} - {elev["nume"]}\n"""
                v=1
        if v==0:
            mesaj = mesaj + f"""`{medii["elevId"]}` - {medii["medie"]}\n"""
    await ctx.send(mesaj)


@bot.command()
async def top5(ctx):
    mediiMax = [{"elevId": "None", "medie": 0}]*5
    for media in mediiElevi:
        if media["medie"] > mediiMax[0]["medie"]:
            mediiMax[4] = mediiMax[3]
            mediiMax[3] = mediiMax[2]
            mediiMax[2] = mediiMax[1]
            mediiMax[1] = mediiMax[0]
            mediiMax[0] = media
        elif media["medie"] > mediiMax[1]["medie"]:
            mediiMax[4] = mediiMax[3]
            mediiMax[3] = mediiMax[2]
            mediiMax[2] = mediiMax[1]
            mediiMax[1] = media
        elif media["medie"] > mediiMax[2]["medie"]:
            mediiMax[4] = mediiMax[3]
            mediiMax[3] = mediiMax[2]
            mediiMax[2] = media
        elif media["medie"] > mediiMax[3]["medie"]:
            mediiMax[4] = mediiMax[3]
            mediiMax[3] = media
        elif media["medie"] > mediiMax[4]["medie"]:
            mediiMax[4] = media
    embed = discord.Embed(title="Cei mai buni 5 elevi din clasa:",
                          color=discord.Color.blue())
    for i in range(0, 5):
        v=0
        for elev in listaElevi.find():
            if mediiMax[i]["elevId"] == elev["elevId"]:
                embed.add_field(name=f"Top {i+1}", value=f"""**{mediiMax[i]["medie"]}** - `{mediiMax[i]["elevId"]}` - {elev["nume"]}""", inline=False)
                v=1
        if v==0:
            embed.add_field(name=f"Top {i+1}", value=f"""**{mediiMax[i]["medie"]}** - `{mediiMax[i]["elevId"]}`""", inline=False)
    embed.set_footer(text="Pentru ajutor contactati: DynoW#9056")
    await ctx.send(embed=embed)


@bot.command()
async def note(ctx, elevId: str):
    mesaj = ""
    for elev in catalog.find():
        if elev["elevId"] == elevId:
            for materi in elev["Materii"]:
                mesaj = mesaj + f"""*{materi["Nume"]}* - """
                for nota in materi["Despre"][0]["data"]:
                    mesaj = mesaj + f"""*{str(round(nota[1]))}*  """
                mesaj = mesaj + "\n"
    await ctx.send(mesaj)


@bot.command()
async def medi(ctx, elevId: str):
    mesaj = ""
    for elev in catalog.find():
        if elev["elevId"] == elevId:
            for medie in elev["Medii"]:
                mesaj = mesaj + f"""*{medie["Nume"]}* - *{str(medie["Nota"])}* - Rang: {medie["Rang"]}\n"""
    await ctx.send(mesaj)
    

@bot.command()
async def sync(ctx):
    calcMedii()
    await ctx.send("Done!")
    
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
