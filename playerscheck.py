import discord
import datetime
from playercheckmethod import PlayerCheckMethod
class PlayersCheck():
   def __init__(self, discordClient):
      self.discordClient = discordClient
      pass
         
   async def Check(self, groupsToCheck, mode, modeArg):
      members = self.discordClient.get_all_members()
      groupsIds = [d['id'] for d in groupsToCheck]
      detectedUsersNames = []
      preLoadedMessages = []
      if mode is PlayerCheckMethod.MESSAGE_ADD:
         for channelsIds in [c['channels'] for c in groupsToCheck]:
            for channelId in channelsIds:
               channel = discord.utils.find(lambda c: c.id == int(channelId), self.discordClient.get_all_channels())
               async for m in channel.history(limit=200).filter(lambda msg: msg.created_at + datetime.timedelta(days=modeArg) > datetime.datetime.now()):
                  preLoadedMessages.append(m)
      for member in members:
         for role in member.roles:
            roleId = str(role.id)
            if roleId in groupsIds:
               if mode is PlayerCheckMethod.JOIN_DATE:
                  if datetime.datetime.now() > member.joined_at + datetime.timedelta(days=modeArg):
                     detectedUsersNames.append(member)
               elif mode is PlayerCheckMethod.MESSAGE_ADD:
                  if datetime.datetime.now() > member.joined_at + datetime.timedelta(days=modeArg):
                     groupDict = [i for i in groupsToCheck if i['id'] == roleId][0]
                     channels = groupDict['channels']
                     message = discord.utils.find(lambda m: m.author == member, preLoadedMessages)
                     if message is None:
                        detectedUsersNames.append(member)
      return detectedUsersNames



                        
      

