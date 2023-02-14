import os
import discord

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

        if message.content.lower() == "!author":
            await message.channel.send(
                "D-bot author: Enrico Francesco Damiani"
                " (enrico.francesco.damiani@gmail.com)"
            )

    else:
        await message.channel.send(
            "In order to talk with me or execute a command, please send a DM!"
        )


client.run(DISCORD_TOKEN)
