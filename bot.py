import os
import re
import secrets

import discord
from discord.ext import commands
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from keep_alive import keep_alive
from private_data import emails as valid_emails

load_dotenv()

def verify_msg(guildname, domains):
    return 

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '.', intents=intents)

def email_check(email):
    regex = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    if re.search(regex, email):
        return True
    else:
        return False

codes = dict()

@client.event
async def on_member_join(member):
    await member.send("Thank you for joining SUMS discord. You need to verify that you are a student at St Andrews to gain access to some channels. **Please reply here with your @st-andrews.ac.uk email address**.")

@client.event
async def on_reaction_add(reaction, users):
    print(reaction, users)



@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not message.guild: # message is DM
        try:
            message_content = message.content.strip()
            if (message.guild == None) and email_check(message_content) and message_content in valid_emails:
                random_code = secrets.token_hex(16) 
                codes[message.author] = random_code
                emailmessage = Mail(
                    from_email=os.environ.get('SENDGRID_EMAIL'),
                    to_emails=message_content,
                    subject='Your verification code',
                    html_content=str(random_code))
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(emailmessage)
                await message.channel.send("Email sent. **Please reply here with your verification code**. If you haven't received it, check your spam folder.")
            elif message_content==codes.get(message.author, None):
                member = client.get_guild(947059344363638794).get_member(message.author.id)
                await member.add_roles(client.get_guild(947059344363638794).get_role(932716153141354567))
                await message.channel.send("Thank you. You have been successfully verfied.")
            elif message.guild == None:
                await message.channel.send("Unsupported command")
        except:
            await message.channel.send('Uh Oh. Looks like the bot has malfunctioned :dizzy_face:. Please get DE0CH#6314\'s attention to ask him to fix it.')
    else:
        await client.process_commands(message)

@client.command()
async def verify(ctx):
    await ctx.author.send("Thank you for verifying yourself. **Please reply here with your @st-andrews.ac.uk email address**.")

keep_alive()
client.run(os.environ.get('DISCORD_TOKEN'))
