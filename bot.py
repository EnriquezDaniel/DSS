import discord.ext.commands

class DSSClient(discord.ext.commands.Bot):
    async def on_connect(self):
        await self.change_presence(status=discord.Status.dnd)

    async def on_ready(self):
        await self.change_presence(status=discord.Status.online)
        print("Client ready")
    
    async def on_disconnect(self):
        await self.change_presence(status=discord.Status.idle)
        # TODO: interrupt all api calls and shutdown the call scheduler

# main for debug
client = DSSClient(command_prefix="!")

# commands
# later on this should implement the discord.py cog feature
# if the amount of commands gets too high
@client.command()
async def ping(context):
    await context.send("Pong!")

@client.command()
async def stop(context):
    await context.bot.logout()

client.run('NjE4NTc1MzEwOTU0Mjk5NDE0.XlDaIw.vYWCqGINnJxRbPmLEf1I8niwfi8')
