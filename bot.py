import discord
from discord import Game
import numpy as np
import time
import asyncio
from discord.ext.commands import Bot

BOT_PREFIX = ("?", "!")
TOKEN = ''

client = Bot(command_prefix=BOT_PREFIX)

# Returns a random number between limits


@client.command(name='roll',
                description="Returns a random number between limits",
                brief="Returns a random number between limits",
                aliases=['random', 'rand'],
                pass_context=True)
async def roll(context, n1, n2):

    await client.say("Here is a random number for " + context.message.author.mention +
                     ": " + str(np.random.randint(n1, n2)))
 # Greets user


@client.command(name='greet',
                description="Returns a greeting",
                brief="Greeting.",
                aliases=['greeting', 'hello'],
                pass_context=True)
async def greet(context):
    greetings = ['Hello', 'How are you?', "What's up?", "Not in a mood for greeting today."]
    msg = '{} {}'.format(np.random.choice(greetings), context.message.author.mention)
    await client.send_message(context.message.channel, msg)


@client.command(name='timer',
                description="Reminder in Hrs:Mins:Secs Chore",
                brief="Reminds you to do your chores",
                aliases=['remind', 'remindme'],
                pass_context=True)
async def timer(context):
    args = context.message.content.split(' ', 2)
    t_hrs, t_mins, t_secs = args[1].split(':')
    t = int(t_hrs) * 3600 + int(t_mins) * 60 + int(t_secs)
    message = args[2]
    await client.say("Reminder set")
    while t:
        await asyncio.sleep(1)
        t -= 1
    await client.send_message(context.message.channel, "Reminder from the past for: " + context.message.author.mention + " " + message)


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    await client.process_commands(message)


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
