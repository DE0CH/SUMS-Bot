import os
import re
import secrets

import discord
from discord.ext import commands
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from keep_alive import keep_alive
from emails import emails as verified_emails


load_dotenv()


intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = commands.Bot(command_prefix = '.', intents=intents)

reaction_roles = {}

reaction_roles[947841356280258600] = {}

with open('reaction_roles_947841356280258600.txt') as f:
    for line in f:
        if line.strip():
            emoji, id = line.split()
            id = int(id)
            reaction_roles[947841356280258600][emoji] = id

@client.event
async def on_raw_reaction_add(reaction):
    if reaction.guild_id == 947059344363638794 and reaction.message_id == 947841356280258600:
        try:
            await reaction.member.add_roles(client.get_guild(947059344363638794).get_role(reaction_roles[947841356280258600][reaction.emoji.name]))
        except KeyError as e:
            pass
        
@client.event
async def on_raw_reaction_remove(reaction):
    if reaction.guild_id == 947059344363638794 and reaction.message_id == 947841356280258600:
        try:
            await reaction.member.remove_roles(client.get_guild(947059344363638794).get_role(reaction_roles[947841356280258600][reaction.emoji.name]))
        except KeyError as e:
            pass    
keep_alive()
client.run(os.environ.get('DISCORD_TOKEN'))
