# Property of JargonBots.
# Written By Armaan Kapoor & Eric (Dan) Karlsson on 12-25-2022.

import discord
import os
from dotenv import load_dotenv
from kcjargon.openai.conversation import conversation_obj

load_dotenv("/Users/armaan/Desktop/kcjargon-main/config/.env")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!'):
        Name = str(message.content[1::])
        cv = conversation(starting_environment="The following is chat with {}.".format(Name), bot_name="{}: ".format(Name))
        await message.author.send("The following is a chat with {}".format(Name))
        await message.author.send(message.content)
        response = await client.wait_for('message')
        print(f'Reponse: {response}')
        await message.author.send('Got it! I will work on it right away.')

client.run(os.getenv('DISCORD_BOT_TOKEN'))
