import os
import discord
import openai
from dotenv import load_dotenv
import typing
import functools

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


def generate_response(messages):
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=messages,
    temperature=1,
    max_tokens=50
    )
    return response.choices[0].text

def translate_to_texting(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "user", "content": "Rewrite the line below, removing proper grammar and punctuation. Keep your message short."},
                {"role": "user", "content": message}
            ],
        temperature=0.5,
        max_tokens=50,
        n=1,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response['choices'][0]['message']['content']

async def run_blocking(blocking_func: typing.Callable, *args, **kwargs) -> typing.Any:
    func = functools.partial(blocking_func, *args, **kwargs)
    return await client.loop.run_in_executor(None, func)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'ping':
        return message.channel.send('pong')

    else:
        print(message.content)
        author = []
        content = []
        messages = ""
        async for msg in message.channel.history(limit=10):
            if msg.content != "":
                messages = ("%s: %s\n" % (msg.author.name, msg.content)) + messages
        messages += "Albot: "
        response = await run_blocking(generate_response, messages)
        response = await run_blocking(translate_to_texting, response)
    await message.channel.send(response) 


client.run(TOKEN)