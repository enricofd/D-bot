import os
import discord
import multiprocessing
from web_search import search
from save_data import save_data
from local_search import local_search
from local_similarity_search import local_similarity_search
from train_generator import main_generator
from generate_text import generate_text

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

last_train = -1


# ---------- Actions ----------

async def handle_source(message):
    await message.channel.send("D-bot source: https://github.com/enricofd/d-bot")


async def handle_author(message):
    await message.channel.send("D-bot author: Enrico Francesco Damiani (enrico.francesco.damiani@gmail.com)")


async def handle_help(message):
    help_text = """
    D-bot help:
    Possible commands:

    - Run:
        Structure: !run xxx
        Description: This command searches the web using the Web Search API (https://rapidapi.com/contextualwebsearch/api/web-search/).
        Arguments:
            xxx -> The value to be searched (NOT optional)

    - Crawl:
        Structure: !crawl xxx
        Description: This command crawls data from the web (it may take a few seconds). Every 100 new links, it trains the generator model.
        Arguments:
            xxx -> The URL to be crawled, more than one can be passed, split by space (NOT optional)

    - Search:
        Structure: !search xxx th=y
        Description: This command searches local data, using an inverted index strategy.
        Arguments:
            xxx -> Words to be searched, more than one can be passed (NOT optional)
            y -> Threshold value (optional, must be a float)

    - WordNet search:
        Structure: !wn_search xxx th=y
        Description: This command searches local data, using a similarity (via WordNet) and inverted index strategy.
        Arguments:
            xxx -> Words to be searched, more than one can be passed (NOT optional)
            y -> Threshold value (optional, must be a float)

    - Generate:
        Structure: !generate xxx th=y
        Description: This command generate a text based on a local data search, using an inverted index strategy as well as beam forming technique.
        Arguments:
            xxx -> Words to be searched, more than one can be passed (NOT optional)
            y -> Threshold value (optional, must be a float)
    """
    await message.channel.send(help_text)


async def handle_run(message):
    search_value = " ".join(message.content.split()[1:])
    results = search(search_value)

    if results:
        await message.channel.send(f"D-bot found the following results for {search_value}:")
        for result in results:
            await message.channel.send(result)
    else:
        await message.channel.send(
            f"D-bot could not find any results for: {search_value}. Please try a different query.")


async def handle_crawl(message):
    global last_train
    crawl_values = message.content.split()[1:]
    result = save_data(crawl_values)

    if result:
        await message.channel.send(
            f"D-bot successfully crawled {result[1]} results, totalizing {result[0]} stored!"
        )

        if result[0] // 100 > last_train:
            last_train += 1
            process = multiprocessing.Process(target=main_generator, args=())
            process.start()
            await message.channel.send("Started model training in a new background process.")

    else:
        await message.channel.send(
            f"D-bot could not crawl one or more of the following URLs: {crawl_values}. Please, copy and paste the URL from your browser."
        )


async def handle_search(message):
    search_values, threshold = parse_search_parameters(message.content)
    results = local_search(search_values, threshold) if threshold else local_search(search_values)

    if results:
        await message.channel.send(f"D-bot found the following results:")
        for title, url in results.items():
            await message.channel.send(f"{title}:\n{url}\n")
    else:
        await message.channel.send(
            f"D-bot could not find a result! Please try crawling more web sites."
        )


async def handle_wn_search(message):
    try:
        search_values, threshold = parse_search_parameters(message.content)

        results = local_similarity_search(search_values, threshold) if threshold else local_similarity_search(
            search_values)
        if results:
            await message.channel.send(f"D-bot found the following results:")
            for title, url in results.items():
                await message.channel.send(f"{title}:\n{url}\n")
        else:
            await message.channel.send(
                f"D-bot could not find a result! Please try crawling more web sites."
            )
    except Exception as e:
        await message.channel.send(
            "D-bot encountered an error while processing the request. Please, try again."
        )


async def handle_generate_text(message):
    search_values, threshold = parse_search_parameters(message.content)
    results = local_search(search_values, threshold) if threshold else local_search(search_values)

    if results:
        generated_text = generate_text([title for title, _ in results.items()][0])
        await message.channel.send(f'{generated_text}')

    else:
        await message.channel.send(f'Sorry I do not know how to answer this.')


# ---------- AUX Function ----------

def parse_search_parameters(content):
    if "th=" in content:
        search_values, threshold = content.split("th=")
        threshold = float(threshold)
        if not -1 <= threshold <= 1:
            raise ValueError("Threshold must be between -1.0 and 1.0")
        threshold = (threshold + 1) / 2
    else:
        search_values = content
        threshold = None
    search_values = " ".join(search_values.split()[1:]).strip()
    return search_values, threshold


# ---------- Main ----------

COMMANDS = {
    "!source": handle_source,
    "!author": handle_author,
    "!help": handle_help,
    "!run": handle_run,
    "!crawl": handle_crawl,
    "!search": handle_search,
    "!wn_search": handle_wn_search,
    "!generate": handle_generate_text,

}


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif isinstance(message.channel, discord.DMChannel):

        command = message.content.split()[0].lower()

        if command in COMMANDS:

            try:
                await COMMANDS[command](message)

            except Exception as e:
                await message.channel.send(f"D-bot could not process the request. Error: {str(e)}")

        else:
            await message.channel.send("D-bot could not understand the command. Please, try again.")


if __name__ == "__main__":
    client.run(DISCORD_TOKEN)
