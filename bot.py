import discord
from discord import Game
import numpy as np
import time
import asyncio
from discord.ext.commands import Bot
import keras
import sys
import pickle
import numpy as np
from keras.models import load_model


def sample(preds, temperature=0.2):
    preds = np.reshape(preds, preds.shape[-1])
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds + 1e-25) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def inference(sent):
    string_length = 20
    string_revised = sent.ljust(string_length)
    return string_revised


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


@client.command(name='q',
                description="Returns a ML generated Quote. (starting_word,number of quotes)",
                brief="Quote.",
                aliases=['qt'],
                pass_context=True)
async def q(context):
    max_len = 20
    word_index = {}
    index2char = {}
    temperature = 0.5

    model_path = ""  # Path to model
    model2 = load_model(model_path)

    # Open word_index.pkl
    with open('', 'rb') as handle:
        word_index = pickle.load(handle)

    for ch in word_index:
        index2char[word_index.get(ch)] = ch

    n_tokens = len(word_index) + 1
    args = context.message.content.split(' ', 2)
    start_word = args[1]
    inference_text = inference(start_word)
    n = (int)(args[2])
    temp = ""
    for i in range(n):
        temp = temp + (inference_text.strip() + " ")
        generated_text = inference_text[:20] + ""
        for i in range(100):
            sampled = np.zeros((1, max_len, n_tokens))
            for t, char in enumerate(generated_text):
                sampled[0, t, word_index[char]] = 1.
            preds = model2.predict(sampled, verbose=0)[0]
            next_index = sample(preds, temperature)
            next_char = index2char[next_index]
            if next_char == '\n':
                break
            generated_text += next_char
            generated_text = generated_text[1:]
            temp = temp + next_char
        temp = temp + '\n'
        temp = temp + '---\n'

    msg = 'Quote for {}\n'.format(context.message.author.mention)
    msg = msg + temp
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
