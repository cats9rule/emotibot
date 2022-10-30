# This example requires the 'message_content' intent.

import discord
import logging
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello') or message.content.startswith('hi'):
        await message.channel.send('Hello!')

client.run(TOKEN, log_handler=handler)
