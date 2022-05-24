import os
import random

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Intents
from discord.ext import commands

import utils

# takes the date and the hour
date, hour = utils.dt_hr()

# first log file
if not os.path.exists("logs"):
    os.mkdir("logs")
os.chdir("logs")

if not os.path.exists(f"{date}.txt"):
    with open(f"{date}.txt", "w") as lg:
        lg.write(
            f"---------FILE DI LOG---------\nDATA CREAZIONE = {date}\nORA CREAZIONE = {hour}\n-----------------------------\n"
        )
else:
    pass

os.chdir(utils.BASE_DIR)

intents = Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="§", intents=intents)

# messages list
with open("frasi.txt", "r", encoding="utf8") as fl:
    frasi_list = fl.readlines()

# emoji
emoji_list = [":fire:", ":books:", ":recycle:"]

scheduler = AsyncIOScheduler()
scheduler.configure(timezone="utc")
scheduler.start()


@bot.event
async def on_ready():
    # change the ID to your channel ID
    # channel = bot.get_channel(CHANNEL_ID)
    channel = bot.get_channel(951156001434914866)
    print(f"canale motivazionale: {channel}")
    utils.write_logs("Start", "Bot started")

    async def send():
        # get a random phrase and a random emoji
        frase = random.choices(frasi_list)[0]
        emoji = random.choices(emoji_list)[0]
        # the message that will be sent
        message = f"""
                    -------------------------
{emoji}   ||@everyone||   {emoji}
-------------------------
**FRASE MOTIVAZIONALE DEL GIORNO**
{frase}
"""

        await channel.send(message)
        print("Messaggio inviato :)")
        utils.write_logs("Message", "Message sent")

    # calls the function everyday
    scheduler.add_job(send, "interval", seconds=3)


# run the bot
bot.run(utils.TOKEN)
