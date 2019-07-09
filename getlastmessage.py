import discord
from getlastmessagemode import GetLastMessageMode
class GetLastMessage():
   def __init__(self, discordClient):
      self.discordClient = discordClient
      pass
   
   async def FindMessageByUser(self, user, where, mode):
      message = None
      channelsToSearch = []
      thisGuild = self.discordClient.guilds[0]
      if mode is GetLastMessageMode.CATEGORIES:
         for categoryId in where:
            category = discord.utils.find(lambda c: str(c.id) == categoryId, thisGuild.categories)
            for channel in category.channels:
               channelsToSearch.append(channel)
      elif mode is GetLastMessageMode.CHANNELS:
         for channelId in where:
            channel = discord.utils.find(lambda c: str(c.id) == channelId, self.discordClient.get_all_channels())
            channelsToSearch.append(channel)

      for channel in channelsToSearch:
         if isinstance(channel, discord.TextChannel):
            try:
               async for m in channel.history(limit=5000).filter(lambda msg: msg.author.id == user.id):
                  if message is None or m.created_at > message.created_at:
                     message = m
            except discord.Forbidden:
               continue
      return message