import discord

class DiscordClientBase(discord.Client):
    def __init__(self, commandExecutor, argparser):
        self.commandExecutor = commandExecutor
        self.argparser = argparser
        super().__init__()

class ExDiscordClient(DiscordClientBase):
    async def on_ready(self):
        activity = discord.Activity(name='graczy przez magiczną kulę', type=discord.ActivityType.watching)
        await self.change_presence(activity=activity)
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message is None or len(message.content) <= 0 or message.author == self.user:
           return
        if message.content[0] == '/':
           data = self.argparser.Parse(message.content)
           await self.commandExecutor.Execute(data[0], message.author, data[1:])