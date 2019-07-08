import discord
from playercheckmethod import PlayerCheckMethod
import asyncio
import datetime
class CheckPlayersTask():
   def __init__(self, discordClient, settingManager, playersCheck):
      self.playersCheck = playersCheck
      self.settingManager = settingManager
      self.discordClient = discordClient
   
   def StartTask(self):
      asyncio.ensure_future(self.CheckPlayers(21600)) 
   
   async def CheckPlayers(self, time):
      while True:
         await asyncio.sleep(time)
         channelToSend = discord.utils.find(lambda c: c.name == "klaudiusz-testing", self.discordClient.get_all_channels())
         channelToSendLog = discord.utils.find(lambda c: c.name == "logi", self.discordClient.get_all_channels())
         #await channelToSend.send("Wysyłane z taska co minutę <3")
         usersWithoutAccept = await self.playersCheck.Check([{'id': '572897687502848034', 'channels': ['572896095374409730']}], PlayerCheckMethod.JOIN_DATE, 2)
         getIdsFromChannelsInCategories = ['573189641797238795', '573189424897064964', '573189367137566750', '573189223608352779', '573189156717592586', '573100293240258629']
         channelsToCheck = []
         thisGuild = self.discordClient.guilds[0]
         for categoryId in getIdsFromChannelsInCategories:
            category = discord.utils.find(lambda c: str(c.id) == categoryId, thisGuild.categories)
            for channel in category.channels:
               channelsToCheck.append(str(channel.id))
         
         inactiveUsers = await self.playersCheck.Check([{'id': '575301044695728158', 'channels': channelsToCheck}], PlayerCheckMethod.MESSAGE_ADD, 5)
         settingObj = self.settingManager.LoadSettings()
         msgForUsersWithoutAccept = settingObj['msgForUsersWithoutCharacter']
         msgForInactiveUsers = settingObj['msgForInactiveUsers']
         for user in usersWithoutAccept:
            if str(user.id) not in settingObj['checkedUsersWithoutAccept']:
               sendedTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
               settingObj['checkedUsersWithoutAccept'][str(user.id)] = sendedTime
               await user.send(msgForUsersWithoutAccept)
               await channelToSendLog.send("<@{0}> otrzymał dnia {1} powiadomienie o braku KP".format(user.id, sendedTime))
         for user in inactiveUsers:
            if str(user.id) not in settingObj['checkedInactiveUsers']:
               sendedTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
               settingObj['checkedInactiveUsers'][str(user.id)] = sendedTime
               await user.send(msgForInactiveUsers)
               await channelToSendLog.send("<@{0}> otrzymał dnia {1} powiadomienie o braku wątku od przynajmniej 5 dni".format(user.id, sendedTime))
         self.settingManager.UpdateSettings(settingObj)


