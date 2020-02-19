import discord
from rpgdiscordhelper.modules.getlastmessagemode import GetLastMessageMode


class LastMessages():
    def __init__(self, discord_client):
        self.discord_client = discord_client
        pass

    async def find_message_by_user(self, server_id, user, where, mode):
        message = None
        channels_to_read = []
        guild = discord.utils.find(
            lambda g: g.id == server_id, self.discord_client.guilds)
        if mode is GetLastMessageMode.CATEGORIES:
            for category_id in where:
                category = discord.utils.find(
                    lambda c: c.id == int(category_id), guild.categories)
                for channel in category.channels:
                    channels_to_read.append(channel)
        elif mode is GetLastMessageMode.CHANNELS:
            for channel_id in where:
                channel = discord.utils.find(
                    lambda c: c.id == int(channel_id), guild.channels)
                channels_to_read.append(channel)

        for channel in channels_to_read:
            if isinstance(channel, discord.TextChannel):
                try:
                    async for m in channel.history(limit=5000).filter(
                            lambda msg: msg.author.id == user.id):
                        if message is None or (
                                m.created_at > message.created_at):
                            message = m
                except discord.Forbidden:
                    continue
        return message
