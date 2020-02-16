import discord
import datetime
from rpgdiscordhelper.modules.playercheckmethod import PlayerCheckMethod
class PlayersCheck():
   def __init__(self, discordClient, settingManager):
      self.discordClient = discordClient
      self.settingManager = settingManager
      pass
         
   async def Check(self, server_id, groupsToCheck, mode, modeArg):
      members = self.discordClient.get_all_members()
      groupsIds = [d['id'] for d in groupsToCheck]
      detectedUsersNames = []
      preLoadedMessages = []
      thisGuild = discord.utils.find(lambda g: g.id == server_id, self.discordClient.guilds)
      if mode is PlayerCheckMethod.MESSAGE_ADD:
         for channelsIds in [c['channels'] for c in groupsToCheck]:
            for channelId in channelsIds:
               channel = discord.utils.find(lambda c: c.id == channelId, thisGuild.channels)
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
                  checkFromDate = member.joined_at
                  if datetime.datetime.now() > checkFromDate + datetime.timedelta(days=modeArg): 
                     message = discord.utils.find(lambda m: m.author == member, preLoadedMessages)
                     if message is None:
                        detectedUsersNames.append(member)
      return detectedUsersNames



                        
      

