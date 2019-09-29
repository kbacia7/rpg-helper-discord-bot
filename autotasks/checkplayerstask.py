import discord
from playercheckmethod import PlayerCheckMethod
from autotasks.base import BaseTask
import asyncio
import datetime
class CheckPlayersTask(BaseTask):
   def __init__(self, discordClient, settingManager, playersCheck):
      self.playersCheck = playersCheck
      self.settingManager = settingManager
      super(CheckPlayersTask, self).__init__(discordClient)

   def Start(self):
      super(CheckPlayersTask, self).Start(21600)
   
   async def Run(self, time):
      while True:
         await asyncio.sleep(time)
         settingObj = self.settingManager.LoadSettings()
         channelToSendLog = discord.utils.find(lambda c: c.id == int(settingObj['channelWithLogs']), self.discordClient.get_all_channels())

         usersWithoutAccept = await self.playersCheck.Check([{'id': settingObj['roleWithPlayersWithoutCharacter'], 'channels': [settingObj['channelWithPlayersCharacters']]}], PlayerCheckMethod.JOIN_DATE, 2)
         getIdsFromChannelsInCategories = settingObj['categoriesForLookingInactivePlayers']
         channelsToCheck = []
         thisGuild = self.discordClient.guilds[0]
         for categoryId in getIdsFromChannelsInCategories:
            category = discord.utils.find(lambda c: str(c.id) == categoryId, thisGuild.categories)
            for channel in category.channels:
               channelsToCheck.append(str(channel.id))
         
         inactiveUsers = await self.playersCheck.Check([{'id': settingObj['roleWithPlayersWithCharacter'], 'channels': channelsToCheck}], PlayerCheckMethod.MESSAGE_ADD, 5)
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
         


