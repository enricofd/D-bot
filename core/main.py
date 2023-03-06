import os
import discord
import re
from web_search import search

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
DISCORD_SERVER = os.environ.get("DISCORD_SERVER")
DISCORD_CHANNEL = os.environ.get("DISCORD_CHANNEL")

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=DISCORD_SERVER)
    channel = discord.utils.get(guild.text_channels, name=DISCORD_CHANNEL)
    await channel.send("D-bot is here!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == "!test":
        await message.channel.send("D-bot is running")

    elif isinstance(message.channel, discord.DMChannel):
        if message.content.lower() == "!source":
            await message.channel.send(
                "D-bot source: https://github.com/enricofd/d-bot"
            )

        elif message.content.lower() == "!author":
            await message.channel.send(
                "D-bot author: Enrico Francesco Damiani"
                " (enrico.francesco.damiani@gmail.com)"
            )

        elif message.content.lower() == "!help":
            await message.channel.send(
                "D-bot help: The bot is expected to run a command following the structure: !run xxx\n"
                "This structure is resposible to search the web using the Web Search API ("
                "https://rapidapi.com/contextualwebsearch/api/web-search/)."
                "\nThe argument is:\nxxx -> the value to be searched\n"
                "Argument xxx is not optional."
            )

        elif re.fullmatch("!run(\s.+)", message.content.lower()):

            try:

                search_value = " ".join(message.content.lower().split(" ")[1::])
                results = search(search_value)
                await message.channel.send(
                    f"D-bot found the following results for {search_value}: "
                )
                for result in results:
                    await message.channel.send(
                        f"{result}"
                    )

            except:
                await message.channel.send(
                    f"D-bot could not process the request for: {search_value}. Please, try again."
                )

        else:
            await message.channel.send(
                f"D-bot could not understand the command. Please, try again."
            )


client.run(DISCORD_TOKEN)
