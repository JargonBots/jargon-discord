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

    # if message.author == client.user:
    #     return

    # actor_name = None
    # cv = None
    in_conversation = False

    if message.content.startswith("!") and not in_conversation:
        in_conversation = True
        actor_name = str(message.content[1::])
        cv = Conversation(starting_environment="The following is a conversation with {}.".format(actor_name), bot_name="{}: ".format(actor_name))

    while message.content != "quit" and in_conversation and message.author != client.user:

        cv.environment += "\nMe: " + str(message.content)
        cv.bot_append()

        await message.author.send(cv.bot_name + cv.toks)

        response = await client.wait_for("message")
        print(f"Reponse: {response}")
        message = response
        in_conversation = True

    if message.content == "quit" and in_conversation and message.author:
        in_conversation = False
        await message.author.send(f"Exited Chat With {actor_name}")
        print(f"Exiting Chat With {actor_name}")
        print("Conversation:\n" + cv.environment)
        return


def run():
    client.run(os.getenv("DISCORD_BOT_TOKEN"))
