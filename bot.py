import json
import discord.ext.commands
#from api import YouTubeAPI
import api

class DSSClient(discord.ext.commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix=command_prefix)

        # initialize all needed APIs
        self.youtube = api.YouTubeAPI()

    async def on_connect(self):
        await self.change_presence(status=discord.Status.dnd)

    async def on_ready(self):
        await self.change_presence(status=discord.Status.online)
        print("Client ready")
    
    async def on_disconnect(self):
        print("Client disconnected")
        # TODO: interrupt all api calls and shutdown the call scheduler
        print("DSS shut down")

# main for debug
client = DSSClient(command_prefix="!")

# commands
# later on this should implement the discord.py cog feature
# if the amount of commands gets too high
# ideas for cog groups: meta (for clear, ping, stop, etc)
#                   and api (all api related commands)
@client.command()
async def ping(context):
    await context.send("Pong!")

@client.command()
async def stop(context):
    await context.bot.change_presence(status=discord.Status.offline)
    # need to change presence here b/c the bot will not be connected during on_disconnect()
    await context.bot.logout()

@client.command()
async def poll(context):
    await context.bot.change_presence(status=discord.Status.idle)
    messages = context.bot.youtube.poll()
    for m in messages:
        await context.send(m)
    await context.bot.change_presence(status=discord.Status.online)

@client.command()
async def clear(context):
    async for m in context.message.channel.history(limit = 100):
        await m.delete()

# testing
if __name__ == "__main__":
    with open("config.json") as config:
        data = json.load(config)
        token = data["discordBotToken"]
        client.run(token)
