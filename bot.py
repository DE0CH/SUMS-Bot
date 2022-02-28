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

def verify_msg(guildname, domains):
    return 

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = commands.Bot(command_prefix = '.', intents=intents)

def email_check(email):
    regex = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    if re.search(regex, email):
        return True
    else:
        return False

codes = dict()
codes_guild = dict()

@client.event
async def on_raw_reaction_add(reaction):
    if reaction.guild_id == 947059344363638794 and reaction.message_id == 947154887370739803:
        member = reaction.member
        if reaction.emoji.name == '2️⃣':
            await member.add_roles(client.get_guild(947059344363638794).get_role(947150257731551242))
        if reaction.emoji.name == '3️⃣':
            await member.add_roles(client.get_guild(947059344363638794).get_role(947150518038433802))
        if reaction.emoji.name == '4️⃣':
            await member.add_roles(client.get_guild(947059344363638794).get_role(947150517598048306))
        if reaction.emoji.name == '5️⃣':
            await member.add_roles(client.get_guild(947059344363638794).get_role(947150562972028928))
        if reaction.emoji.name == '6️⃣':
            await member.add_roles(client.get_guild(947059344363638794).get_role(947150581674434600))
    if reaction.guild_id == 947059344363638794 and reaction.message_id == 947159949849542666:
        if reaction.emoji.name == '✅':
            author = reaction.member
            codes[author.id] = secrets.token_hex(16)
            codes_guild[codes[author.id]] = 947059344363638794
            await author.send("Thank you for verifying yourself. **Please reply here with your registered email address (to where we have sent you SUMO emails)**.")

@client.event
async def on_raw_reaction_remove(reaction):
    if reaction.guild_id == 947059344363638794 and reaction.message_id == 947154887370739803:
        member = client.get_guild(947059344363638794).get_member(reaction.user_id)
        if reaction.emoji.name == '2️⃣':
            await member.remove_roles(client.get_guild(947059344363638794).get_role(947150257731551242))
        if reaction.emoji.name == '3️⃣':
            await member.remove_roles(client.get_guild(947059344363638794).get_role(947150518038433802))
        if reaction.emoji.name == '4️⃣':
            await member.remove_roles(client.get_guild(947059344363638794).get_role(947150517598048306))
        if reaction.emoji.name == '5️⃣':
            await member.remove_roles(client.get_guild(947059344363638794).get_role(947150562972028928))
        if reaction.emoji.name == '6️⃣':
            await member.remove_roles(client.get_guild(947059344363638794).get_role(947150581674434600))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not message.guild: # message is DM
        try:
            message_content = message.content.strip()
            if email_check(message_content) and \
                ((codes_guild.get(codes.get(message.author.id, None), None) == 876437717142106222 and message_content.endswith("st-andrews.ac.uk")) or \
                (codes_guild.get(codes.get(message.author.id, None), None) == 947059344363638794 and message_content.lower() in verified_emails)):
                random_code = codes[message.author.id]
                emailmessage = Mail(
                    from_email=os.environ.get('SENDGRID_EMAIL'),
                    to_emails=message_content,
                    subject='Your verification code',
                    html_content=str(random_code))
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(emailmessage)
                await message.channel.send("Email sent. **Please reply here with your verification code**. If you haven't received it, check your spam folder.")
            elif message_content==codes.get(message.author.id, None):
                if codes_guild[message_content] == 876437717142106222:
                    member = client.get_guild(876437717142106222).get_member(message.author.id)
                    await member.add_roles(client.get_guild(876437717142106222).get_role(932716153141354567))
                elif codes_guild[message.content] == 947059344363638794:
                    member = client.get_guild(947059344363638794).get_member(message.author.id)
                    await member.remove_roles(client.get_guild(947059344363638794).get_role(947063929438367774))
                await message.channel.send("Thank you. You have been successfully verified.")
            elif message.guild == None:
                await message.channel.send("Unsupported command")
        except Exception as e:
            await message.channel.send('Uh Oh. Looks like the bot has malfunctioned :dizzy_face:. Please get DE0CH#6314\'s attention to ask him to fix it.')
            raise e
    else:
        await client.process_commands(message)

@client.command()
async def verify(ctx):
    if ctx.guild.id == 876437717142106222:
        codes[ctx.author.id] = secrets.token_hex(16)
        codes_guild[codes[ctx.author.id]] = 876437717142106222
        await ctx.author.send("Thank you for verifying yourself. **Please reply here with your @st-andrews.ac.uk email address**.")

keep_alive()
client.run(os.environ.get('DISCORD_TOKEN'))
