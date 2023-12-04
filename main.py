import discord
import requests
import json
from cogs import test

json_open = open('key.json', 'r')
json_load = json.load(json_open)
TOKEN = json_load['TOKEN']

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot is ready!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return  
    
    res = test.main()
    await message.channel.send(res)

client.run(TOKEN)
