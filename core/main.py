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
                "D-bot help: The bot is expected to run a command following the structure: !run \'%xxx% yyy zzz\'.\n"
                "This structure is resposible to search the web using the Web Search API ("
                "https://rapidapi.com/contextualwebsearch/api/web-search/)."
                "\nThe arguments are:\nxxx -> the value to be searched (must be enclosed by \'%\')\n"
                "yyy -> page number (must be an integer)\nzzz -> page size (must be an inter).\n"
                "Arguments yyy and zzz are optional while xxx is not."
            )

        elif re.fullmatch("!run(\s%.+%)(\s\w+){0,2}", message.content.lower()):

            try:
                arguments = message.content.lower().split("%")[1::]

                search_value = arguments[0]

                if len(arguments) > 1:
                    arguments_modify = arguments[1].split(" ")
                    arguments_size = len(arguments_modify)

                    if arguments_size == 1:
                        page_number = arguments_modify[0]
                        results = await search(search_value, page_number)

                    elif arguments_size == 2:
                        page_number = arguments_modify[0]
                        page_size = arguments_modify[1]
                        results = await search(search_value, page_number, page_size)

                    else:
                        raise IndexError

                else:
                    results = await search(search_value)

                await message.channel.send(
                    f"D-bot web search result: {results}"
                )

            except:
                await message.channel.send(
                    f"D-bot could not process the request. Please, try again. You may use !help to better run a command."
                )

        else:
            await message.channel.send(
                f"D-bot could not understand the command. Please, try again. You may use !help to better run a command."
            )


client.run(DISCORD_TOKEN)
