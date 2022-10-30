import discord
import logging
import os
from dotenv import load_dotenv
import emotion_detection.detector as detector

def connect():
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
    async def on_guild_join(guild):
        for channel in guild.text_channels:
            print(channel)
            if channel.name == "general":
                await channel.send("Hello, I am Emotibot and I stalk your emotions. Also, I only understand English cuz I'm dumb (for now).")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('hello') or message.content.startswith('hi'):
            await message.channel.send('Hello!')

        emotion = detector.predict_emotion(message.content)
        print(emotion)
        quote = detector.generate_quote(emotion)
        if quote != "":
            await message.channel.send(quote)
        


    client.run(TOKEN, log_handler=handler)
