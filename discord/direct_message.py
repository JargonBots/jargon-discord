import discord
import os

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

    if message.content.startswith('hello'):
        await message.author.send('Hi there!')
        await message.author.send('What can I do for you?')
        response = await client.wait_for('message')
        print(f'Reponse: {response}')
        await message.author.send('Got it! I will work on it right away.')

client.run(os.getenv('DISCORD_BOT_TOKEN'))