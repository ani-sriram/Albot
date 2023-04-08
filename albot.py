import os
import discord
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'ping':
        await message.channel.send('pong')

    else:
        print(message.content)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    #{"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message.content},
                    #{"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                    #{"role": "user", "content": "Where was it played?"}
                ],
            temperature=0.5,
            max_tokens=150,
            n=1,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        await message.channel.send(response['choices'][0]['message']['content'])

client.run(TOKEN)