import discord
from rpgdiscordhelper.modules.playercheckmethod import PlayerCheckMethod
from rpgdiscordhelper.autotasks.base import BaseTask
import asyncio
import datetime
from rpgdiscordhelper.modules.settingname import SettingName

class CheckPlayersTask(BaseTask):
   def __init__(self, discordClient, settingManager, playersCheck):
      self.playersCheck = playersCheck
      self.settingManager = settingManager
      super(CheckPlayersTask, self).__init__(discordClient)

   def Start(self, server_id):
      super(CheckPlayersTask, self).Start(server_id, 21600)
   
   async def Run(self, server_id, time, channel):
      while True:
         await asyncio.sleep(time)
         settingObj = self.settingManager.LoadSettings(server_id)
         thisGuild = discord.utils.find(lambda g: g.id == int(server_id), self.discordClient.guilds)
         channelToSendLog = discord.utils.find(lambda c: c.id == int(settingObj[SettingName.LOGS_CHANNEL_ID.value]), thisGuild.channels)

         usersWithoutAccept = await self.playersCheck.Check(server_id, [
            {'id': settingObj[SettingName.PLAYER_WITHOUT_CHARACTER_ROLE_ID.value], 'channels': [settingObj[SettingName.PLAYER_WITH_CHARACTER_ROLE_ID.value]]}
         ], PlayerCheckMethod.JOIN_DATE, 2)
         getIdsFromChannelsInCategories = settingObj[SettingName.CATEGORY_FOR_LOOKING_PLAYERS.value]
         channelsToCheck = []
         for categoryId in getIdsFromChannelsInCategories:
            category = discord.utils.find(lambda c: str(c.id) == categoryId, thisGuild.categories)
            for c in category.channels:
               channelsToCheck.append(c.id)
         
         inactiveUsers = await self.playersCheck.Check(server_id, [
            {'id': settingObj[SettingName.PLAYER_WITH_CHARACTER_ROLE_ID.value], 'channels': channelsToCheck}
         ], PlayerCheckMethod.MESSAGE_ADD, 5)
         msgForUsersWithoutAccept = settingObj[SettingName.MESSAGE_FOR_PLAYERS_WITHOUT_CHARACTER.value]
         msgForInactiveUsers = settingObj[SettingName.MESSAGE_FOR_INACTIVE_PLAYERS.value]
         for user in usersWithoutAccept:
            if str(user.id) not in settingObj['checkedUsersWithoutAccept']:
               sendedTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
               settingObj['checkedUsersWithoutAccept'][str(user.id)] = sendedTime
               await user.send(msgForUsersWithoutAccept)
               await channelToSendLog.send("<@{0}> got reminder at {1} that still doesn't have created character".format(user.id, sendedTime))
         for user in inactiveUsers:
            if str(user.id) not in settingObj['checkedInactiveUsers']:
               sendedTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
               settingObj['checkedInactiveUsers'][str(user.id)] = sendedTime
               await user.send(msgForInactiveUsers)
               await channelToSendLog.send("<@{0}> got reminder at {1} that doesn't have any active game from minimum 5 days".format(user.id, sendedTime))
         self.settingManager.UpdateSettings(settingObj)
         


