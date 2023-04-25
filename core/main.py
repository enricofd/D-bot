# Help
# Ensaio

import os
import discord
import re
from web_search import search
from save_data import save_data
from local_search import local_search
from local_similarity_search import local_similarity_search

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
                "D-bot help:\nPossible commands:\n\n   - Run:\n      "
                " Structure: !run xxx\n       Description: This structure is"
                " resposible to search the web using the Web Search API"
                " (https://rapidapi.com/contextualwebsearch/api/web-search/).\n"
                "       Arguments:\n           xxx -> The value to be searched"
                " (NOT optional)\n\n   - Crawl:\n       Structure: !crawl"
                " xxx\n       Description: This structure is resposible to"
                " crawl data from the web (it may take a few seconds).\n      "
                " Arguments:\n           xxx -> The url to be crawled, more"
                " than one can be passes, splited by space (NOT optional)\n\n "
                "  - Search:\n       Structure: !search xxx\n      "
                " Description: This structure is resposible to search local"
                " data, using an inverted index strategy.\n       Arguments:\n"
                "           xxx -> Words to be searched, more than one can be"
                " passes(NOT optional)\n\n  - WordNet search:\n      "
                " Structure: !wn_search xxx\n       Description: This"
                " structure is resposible to search local data, using a"
                " similarity (via WordNet) and inverted index strategy.\n     "
                "  Arguments:\n           xxx -> Words to be searched, more"
                " than one can be passes(NOT optional)\n\n"
            )

        elif re.fullmatch("!run(\s.+)", message.content.lower()):

            try:

                search_value = " ".join(
                    message.content.lower().split(" ")[1::]
                )
                results = search(search_value)
                await message.channel.send(
                    f"D-bot found the following results for {search_value}: "
                )
                for result in results:
                    await message.channel.send(f"{result}")

            except:
                await message.channel.send(
                    f"D-bot could not process the request for: {search_value}."
                    " Please, try again."
                )

        elif re.fullmatch("!crawl(\s.+)", message.content.lower()):
            try:
                crawl_values = message.content.lower().split(" ")[1::]
                result = save_data(crawl_values)

                if result:
                    await message.channel.send(
                        f"D-bot successfully crawled {result[1]} results,"
                        f" totalizing {result[0]} stored!"
                    )

                else:
                    await message.channel.send(
                        "D-bot could not crawl one of the following:"
                        f" {crawl_values}. Please, copy and paste the URL from"
                        " your browser."
                    )

            except:
                await message.channel.send(
                    f"D-bot could not process the request for: {crawl_values}."
                    " Please, try again."
                )

        elif re.fullmatch("!search(\s((?!th.)\w+))+(\sth=\d+\.\d+)?", message.content.lower()):
            try:
                th: str = message.content.lower().split("th=")[-1] if len(message.lower().split("th=")) > 1 else None

                if th:
                    if -1 <= float(th) <= 1:
                        text = " ".join(message.lower().split("th=")[:-1])
                        search_values = " ".join(
                            text.split(" ")[1::]
                        ).strip()
                        results = local_search(search_values, (float(th) + 1) / 2)

                    else:
                        await message.channel.send(
                            f"Please, make sure -1.0 >= th <= 1.0"
                        )

                else:
                    search_values = " ".join(
                        message.content.lower().split(" ")[1::]
                    )
                    results = local_search(search_values)

                if results:
                    await message.channel.send(
                        f"D-bot successfully results:\n"
                    )
                    for title, url in results.items():
                        await message.channel.send(f"{title}:\n{url}\n")

                else:
                    await message.channel.send(
                        f"D-bot could not find a result! Please try crawling"
                        f" more web sites."
                    )

            except:
                await message.channel.send(
                    "D-bot could not process the request for:"
                    f" {search_values}. Please, try again."
                )

        elif re.fullmatch("!wn_search(\s((?!th.)\w+))+(\sth=\d+\.\d+)?", message.content.lower()):
            try:
                th: str = message.content.lower().split("th=")[-1] if len(message.lower().split("th=")) > 1 else None

                if th:
                    if -1 <= float(th) <= 1:
                        text = " ".join(message.lower().split("th=")[:-1])
                        search_values = " ".join(
                            text.split(" ")[1::]
                        ).strip()
                        results = local_similarity_search(search_values, (float(th) + 1) / 2)

                    else:
                        await message.channel.send(
                            f"Please, make sure -1.0 >= th <= 1.0"
                        )

                else:
                    search_values = " ".join(
                        message.content.lower().split(" ")[1::]
                    )
                    results = local_similarity_search(search_values)

                if results:
                    await message.channel.send(
                        f"D-bot successfully results:\n"
                    )
                    for title, url in results.items():
                        await message.channel.send(f"{title}:\n{url}\n")

                else:
                    await message.channel.send(
                        f"D-bot could not find a result! Please try crawling"
                        f" more web sites."
                    )

            except:
                await message.channel.send(
                    "D-bot could not process the request for:"
                    f" {search_values}. Please, try again."
                )

        else:
            await message.channel.send(
                f"D-bot could not understand the command. Please, try again."
            )


client.run(DISCORD_TOKEN)
