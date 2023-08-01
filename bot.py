import discord
from discord.ext import commands
from datetime import datetime
from datetime import datetime, timedelta
import pymongo
from decouple import config
import urllib.parse

mongo_user = urllib.parse.quote_plus(config("MONGO_USER"))
mongo_pass = urllib.parse.quote_plus(config("MONGO_PASSWORD"))
myclient = pymongo.MongoClient(
    "mongodb+srv://%s:%s@cluster0.lk2h7ri.mongodb.net/?retryWrites=true&w=majority"
    % (mongo_user, mongo_pass)
)
db = myclient["db-catalog"]
catalog = db["catalog"]
listaElevi = db["elevi"]
materiile = db["materii"]

# Env variables --------------------------------------------------------------------------------------------------------
bot = commands.Bot(
    command_prefix="$",
    description="Comenzi pentru DynoW BOT:",
    help_command=commands.DefaultHelpCommand(no_category="Help"),
    intents=discord.Intents.all(),
)


# Events ---------------------------------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online, activity=discord.Game(name="$help | dynow.tk/bot")
    )
    await bot.add_cog(Fun())
    await bot.add_cog(Catalog())
    await bot.tree.sync()
    print("\x1B[36mStatus\x1B[0m: " + "Bot is online!")
    for guild in bot.guilds:
        print("\x1B[95mServer\x1B[0m: " + guild.name)


# Functions ------------------------------------------------------------------------------------------------------------
def calcMedii():
    global mediiElevi
    mediiElevi = []
    for elev in catalog.find():
        sumaMedii = 0
        v = 0
        for medie in elev["Medii"]:
            sumaMedii = sumaMedii + round(medie["Nota"] + 0.09)
        averageMedii = (sumaMedii + 10) / (len(elev["Medii"]) + 1)
        for elev2 in listaElevi.find():
            if elev2["elevId"] == elev["elevId"]:
                mediiElevi.append(
                    {
                        "elevId": elev["elevId"],
                        "nume": elev2["nume"],
                        "medie": round(averageMedii, 2),
                    }
                )
                v = 1
        if v == 0:
            mediiElevi.append(
                {
                    "elevId": elev["elevId"],
                    "nume": None,
                    "medie": round(averageMedii, 2),
                }
            )


calcMedii()


# Commands -------------------------------------------------------------------------------------------------------------
class Fun(commands.Cog):
    """Comenzi amuzante"""

    @commands.command()
    async def ping(self, ctx):
        """Returns a pong!"""
        await ctx.send("pong")

    @commands.command()
    async def zile(self, ctx, obj):
        """scoala | vacanta | bac"""
        if obj != "scoala" and obj != "vacanta" and obj != "bac":
            await ctx.send("Foloseste: *$zile scoala/vacanta/bac*")
        else:
            current_time = datetime.now()
            if obj == "scoala":
                momentspecial = datetime(2023, 6, 15)
                weekdays = 0
                while current_time.date() < momentspecial.date():
                    if current_time.weekday() < 5:  # Monday to Friday are weekdays
                        weekdays += 1
                    current_time += timedelta(days=1)
                await ctx.send(f"Mai sunt {weekdays} zile de scoala.")
            elif obj == "vacanta":
                momentspecial = datetime(2023, 6, 15)
                remaining_days = (momentspecial - current_time).days
                await ctx.send(f"Mai sunt {remaining_days} zile pana la vacanta.")
            elif obj == "bac":
                momentspecial = datetime(2025, 6, 12)
                remaining_days = (momentspecial - current_time).days
                await ctx.send(f"Mai sunt {remaining_days} zile pana la bac.")


# Catalog commands -----------------------------------------------------------------------------------------------------
class Catalog(commands.Cog):
    """Comenzi pentru catalog"""

    @commands.command()
    async def all(self, ctx):
        """Vezi toate id-urile"""
        mesaj = ""
        for medii in mediiElevi:
            if medii["nume"] != None:
                mesaj = (
                    mesaj
                    + f"""`{medii["elevId"]}` - {medii["medie"]} - {medii["nume"]}\n"""
                )
            else:
                mesaj = mesaj + f"""`{medii["elevId"]}` - {medii["medie"]}\n"""
        await ctx.send(mesaj)

    @commands.command()
    async def list(self, ctx):
        """Vezi mediile ordonate descrescator"""
        mesaj = ""
        listaMedi = []
        for medii in mediiElevi:
            v = 0
            if medii["nume"] != None:
                listaMedi = listaMedi + [
                    [medii["elevId"], medii["medie"], medii["nume"]]
                ]
            else:
                listaMedi = listaMedi + [[medii["elevId"], medii["medie"], None]]
        for i in range(28):
            for j in range(0, 28 - i - 1):
                if listaMedi[j][1] < listaMedi[j + 1][1]:
                    listaMedi[j], listaMedi[j + 1] = listaMedi[j + 1], listaMedi[j]
        for elev in listaMedi:
            if elev[2] != None:
                mesaj = mesaj + f"""`{elev[0]}` - **{elev[1]}** - {elev[2]}\n"""
            else:
                mesaj = mesaj + f"""`{elev[0]}` - **{elev[1]}**\n"""
        await ctx.send(mesaj)

    @commands.command()
    async def elevi(self, ctx):
        """Vezi toti elevii"""
        mesaj = ""
        for elev in listaElevi.find():
            if elev["elevId"] != "":
                mesaj = (
                    mesaj + f"""{elev["$id"]}. {elev["nume"]} - `{elev["elevId"]}`\n"""
                )
            else:
                mesaj = mesaj + f"""{elev["$id"]}. {elev["nume"]} - \n"""
        await ctx.send(mesaj)

    @commands.command()
    async def top(self, ctx):
        """Afiseaza premiile si mentiunule la final de an"""

        mediiMax = [[{"elevId": "None", "medie": 0}]] * 6
        for media in mediiElevi:
            if media["medie"] > mediiMax[0][0]["medie"]:
                mediiMax[5] = mediiMax[4]
                mediiMax[4] = mediiMax[3]
                mediiMax[3] = mediiMax[2]
                mediiMax[2] = mediiMax[1]
                mediiMax[1] = mediiMax[0]
                mediiMax[0] = [media]
            elif media["medie"] == mediiMax[0][0]["medie"]:
                mediiMax[0] = mediiMax[0] + [media]
            elif media["medie"] > mediiMax[1][0]["medie"]:
                mediiMax[5] = mediiMax[4]
                mediiMax[4] = mediiMax[3]
                mediiMax[3] = mediiMax[2]
                mediiMax[2] = mediiMax[1]
                mediiMax[1] = [media]
            elif media["medie"] == mediiMax[1][0]["medie"]:
                mediiMax[1] = mediiMax[1] + [media]
            elif media["medie"] > mediiMax[2][0]["medie"]:
                mediiMax[5] = mediiMax[4]
                mediiMax[4] = mediiMax[3]
                mediiMax[3] = mediiMax[2]
                mediiMax[2] = [media]
            elif media["medie"] == mediiMax[2][0]["medie"]:
                mediiMax[2] = mediiMax[2] + [media]
            elif media["medie"] > mediiMax[3][0]["medie"]:
                mediiMax[5] = mediiMax[4]
                mediiMax[4] = mediiMax[3]
                mediiMax[3] = [media]
            elif media["medie"] == mediiMax[3][0]["medie"]:
                mediiMax[3] = mediiMax[3] + [media]
            elif media["medie"] > mediiMax[4][0]["medie"]:
                mediiMax[5] = mediiMax[4]
                mediiMax[4] = [media]
            elif media["medie"] == mediiMax[4][0]["medie"]:
                mediiMax[4] = mediiMax[4] + [media]
            elif media["medie"] > mediiMax[5][0]["medie"]:
                mediiMax[5] = [media]
            elif media["medie"] == mediiMax[5][0]["medie"]:
                mediiMax[5] = mediiMax[5] + [media]
        embed = discord.Embed(
            title="Premiile de la final de an sunt:", color=discord.Color.blue()
        )
        listaPremii = [
            "Premiul I",
            "Premiul II",
            "Premiul III",
            "Mentiune I",
            "Mentiune II",
            "Mentiune III",
        ]
        listaTrofee = ["🥇", "🥈", "🥉", "🎖️", "🎖️", "🎖️"]
        for i in range(0, 6):
            v = 0
            size = len(mediiMax[i])
            mesaj = ""
            for j in range(0, size):
                if mediiMax[i][j]["nume"] != None:
                    mesaj = (
                        mesaj
                        + f"""**{mediiMax[i][j]["medie"]}** - `{mediiMax[i][j]["elevId"]}` - {mediiMax[i][j]["nume"]}\n"""
                    )
                else:
                    mesaj = (
                        mesaj
                        + f"""**{mediiMax[i][j]["medie"]}** - `{mediiMax[i][j]["elevId"]}`\n"""
                    )
            embed.add_field(
                name=f"{listaTrofee[i]} {listaPremii[i]}", value=mesaj, inline=False
            )
        embed.set_footer(text="Pentru ajutor contactati: DynoW#9056")
        await ctx.send(embed=embed)

    @commands.command()
    async def materii(self, ctx):
        """Vezi media clasei la fiecare materie"""
        embed = discord.Embed(
            title="Media clasei la fiecare materie:", color=discord.Color.blue()
        )
        for materie in materiile.find():
            avgmaterie = 0
            for elev in catalog.find():
                for i in range(0, 17):
                    if elev["Medii"][i]["Nume"] == materie["Nume"]:
                        avgmaterie = avgmaterie + elev["Medii"][i]["Nota"]
            avgmaterie = avgmaterie / 28
            embed.add_field(
                name=materie["Nume2"],
                value=f" - **{round(avgmaterie, 2)}**",
                inline=True,
            )
        embed.set_footer(text="Pentru ajutor contactati: DynoW#9056")
        await ctx.send(embed=embed)

    @commands.command()
    async def medi(self, ctx, elevId: str = None):
        """[id_elev] - Verifica mediile cuiva"""
        if elevId is None:
            await ctx.send("Foloseste: *$medi [id_elev]*")
        elif int(elevId) < 304772 or int(elevId) > 304800:
            await ctx.send(
                "[id_elev] gresit, foloseste $all pentru a vedea toate id-urile"
            )
        else:
            mesaj = ""
            for elev in catalog.find():
                if elev["elevId"] == elevId:
                    for medie in elev["Medii"]:
                        for materie in materiile.find():
                            if materie["Nume"] == medie["Nume"]:
                                mesaj = (
                                    mesaj
                                    + f"""*{materie["Nume2"]}* - *{str(medie["Nota"])}* - Rang: {medie["Rang"]}\n"""
                                )
            await ctx.send(mesaj)

    @commands.command()
    async def note(self, ctx, elevId: str = None):
        """[id_elev] - Verifica notele cuiva"""
        if elevId is None:
            await ctx.send("Foloseste: *$medi [id_elev]*")
        elif int(elevId) < 304772 or int(elevId) > 304800:
            await ctx.send(
                "[id_elev] este gresit, foloseste $all pentru a vedea toate id-urile"
            )
        else:
            mesaj = ""
            for elev in catalog.find():
                if elev["elevId"] == elevId:
                    for materi in elev["Materii"]:
                        for materie in materiile.find():
                            if materie["Nume3"] == materi["Nume"]:
                                mesaj = mesaj + f"""*{materie["Nume2"]}* - """
                        for nota in materi["Despre"][0]["data"]:
                            mesaj = mesaj + f"""*{str(round(nota[1]))}*  """
                        mesaj = mesaj + "\n"
            await ctx.send(mesaj)

    @commands.command()
    async def search(self, ctx, *args: int):
        """[nota1] [nota2] ... - Cauta o persoana folosind notele la matematica"""
        if len(args) == 0:
            await ctx.send(
                "Foloseste: *$search [nota1] [nota2] [nota3] ... (la matematica)*"
            )
        else:
            mesaj = ""
            note = []
            for nota in args:
                note = note + [nota]
            for elev in catalog.find():
                if len(elev["Materii"][0]["Despre"][0]["data"]) == len(note):
                    ok = 1
                    for i in range(0, len(note)):
                        if (
                            round(elev["Materii"][0]["Despre"][0]["data"][i][1], 0)
                            != note[i]
                        ):
                            ok = 0
                    if ok == 1:
                        mesaj = mesaj + elev["elevId"] + "\n"
            if mesaj == "":
                await ctx.send("Nu a fost gasit un elev cu aceste note la matematica!")
            else:
                await ctx.send("Id-ul elevului poate fi:\n" + mesaj)


@bot.tree.command()
async def sync(interaction: discord.Interaction):
    """Sinconizare cu baza de date"""
    calcMedii()
    await interaction.response.send_message("Done!")


# Listening events -----------------------------------------------------------------------------------------------------
@bot.listen()
async def on_message(message):
    if "ntza" in message.content.lower():
        await message.channel.send("Dyno BOT V2.1 is here!")
    if "test" in message.content.lower():
        await message.add_reaction("<💩>")
    if "andreea" in message.content.lower():
        await message.add_reaction("<:Alex:953951303187431455>")
    if "care" in message.content.lower() and message.author.id == 494105470714511360:
        await message.channel.send("pe care")
    if "sex" in message.content.lower() and message.author.id == 257061276486729728:
        await message.channel.send("<:Alex:953951303187431455>")
    if "kill" in message.content.lower():
        if message.author.id == 455608238335983617:
            await message.channel.send("I'M DEAD 💀")
            await bot.change_presence(status=discord.Status.invisible)
        else:
            await message.channel.send("Ur not my boss :middle_finger:")
    if "revive" in message.content.lower():
        if message.author.id == 455608238335983617:
            await message.channel.send("I'M ALIVE 🥹")
            await bot.change_presence(
                status=discord.Status.online,
                activity=discord.Game(name="$help | dynow.tk/bot"),
            )
        else:
            await message.channel.send("Ur not my boss :middle_finger:")
    if "shutdown" in message.content.lower():
        if message.author.id == 455608238335983617:
            mesaj = await message.channel.send("SHUTTING DOWN")
            await mesaj.edit(content="SHUTTING DOWN.")
            await mesaj.edit(content="SHUTTING DOWN..")
            await mesaj.edit(content="SHUTTING DOWN...")
            exit(0)
        else:
            await message.channel.send("You don't have permission")


# Token ----------------------------------------------------------------------------------------------------------------
bot.run(config("DISCORD_BOT_TOKEN"))
