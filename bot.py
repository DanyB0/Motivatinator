import os
import random
from os import getenv

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("TOKEN")

intents = Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# messages list
with open("frasi.txt", "r", encoding="utf8") as fl:
    frasi = fl.readlines()

scheduler = AsyncIOScheduler()
scheduler.configure(timezone="utc")
scheduler.start()


@bot.event
async def on_ready():
    # change the ID to your channel ID
    # channel = bot.get_channel(CHANNEL_ID)
    channel = bot.get_channel(951156001434914866)
    print(channel)

    async def send():
        # get a random number that will be the index of the message in the list
        i = random.randint(0, len(frasi) - 1)
        await channel.send(f"Stay motivated!:\n\n***{frasi[i]}***")
        print("Messaggio inviato :)")

    # calls the function everyday
    scheduler.add_job(send, "interval", seconds=5)


# run the bot
bot.run(TOKEN)
