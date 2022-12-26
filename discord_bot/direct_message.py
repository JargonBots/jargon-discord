# Property of JargonBots.
# Written By Armaan Kapoor & Erik Karlsson on 12-25-2022.

import os

import discord

# from kcjargon.openai.conversation import conversation_obj
from dotenv import load_dotenv
import sys
from os import path
jargonai_dir = "/jargonai/jargonai"
if path.isdir(jargonai_dir):
    sys.path.insert(0, jargonai_dir)
    from conversation import Conversation

load_dotenv()


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):

    if message.author == client.user:
        return
    # actor_name = None
    # cv = None
    in_conversation = False

    if message.content.startswith("!"):
        in_conversation = True
        actor_name = str(message.content[1::])
        cv = Conversation(starting_environment="The following is chat with {}.".format(actor_name), bot_name="{}: ".format(actor_name))
        # await message.author.send("The following is a chat with {}".format(Name))
        # await message.author.send(message.content)
    
    while message.content != "quit" and in_conversation:
        cv.environment += "\nMe: " + str(message.content)
        cv.bot_append()
        await message.author.send(cv.bot_name + cv.toks)
        response = await client.wait_for("message")
        print(f"Reponse: {response}")
        message = response

    if message.content == "quit" and in_conversation:
        in_conversation = False
        print(f"Exiting Chat With {actor_name}")
        print("Conversation: " + cv.environment)
        return


def run():
    client.run(os.getenv("DISCORD_BOT_TOKEN"))
