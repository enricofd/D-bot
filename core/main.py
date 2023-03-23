import os
import discord
import re
from web_search import search
from save_data import save_data

# DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
# DISCORD_SERVER = os.environ.get("DISCORD_SERVER")
# DISCORD_CHANNEL = os.environ.get("DISCORD_CHANNEL")

DISCORD_TOKEN = "MTA3NTA0MDE2NTE4NzI5MzI3NA.GsKcz4.nrHD_r2sP4HlSmu6Hw1Z6Ah9sLb17p92NElT8w"
DISCORD_SERVER = "A Cidade dos Robôs"
DISCORD_CHANNEL = "bot-fest"

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
                "D-bot help:\n"
                "Possible commands:\n\n"
                "   - run:\n"
                "       Structure: !run xxx\n"
                "       Description: This structure is resposible to search the web using the Web Search API (https://rapidapi.com/contextualwebsearch/api/web-search/).\n"
                "       Arguments:\n"
                "           xxx -> The value to be searched (NOT optional)\n"
                "\n"
                "   - crawl:\n"
                "       Structure: !crawl xxx\n"
                "       Description: This structure is resposible to crawl data from the web.\n"
                "       Arguments:\n"
                "           xxx -> The url to be crawled, more than one can be passes, splited by space (NOT optional)\n"
                "\n"
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

        elif re.fullmatch("!crawl(\s.+)", message.content.lower()):
            # try:
            crawl_values = message.content.lower().split(" ")[1::]
            result = save_data(crawl_values)
                
            if result:
                await message.channel.send(
                    f"D-bot successfully crawled {result} results!"
                )
            
            else:
                await message.channel.send(
                    f"D-bot could not crawl one of the following: {crawl_values}. Please, copy and paste the URL from your browser."
                )

            # except:
            #     await message.channel.send(
            #         f"D-bot could not process the request for: {crawl_values}. Please, try again."
            #     )

        else:
            await message.channel.send(
                f"D-bot could not understand the command. Please, try again."
            )


client.run(DISCORD_TOKEN)
