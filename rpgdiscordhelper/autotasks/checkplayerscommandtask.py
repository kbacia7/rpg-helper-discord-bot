import discord
from rpgdiscordhelper.modules.playercheckmethod import PlayerCheckMethod
from rpgdiscordhelper.autotasks.base import BaseTask
from rpgdiscordhelper.modules.getlastmessagemode import GetLastMessageMode
from rpgdiscordhelper.modules.settingname import SettingName
import datetime

class CheckPlayersCommandTask(BaseTask):
   def __init__(self, discordClient, settingManager, playersCheck, getLastMessage):
      self.settingManager = settingManager
      self.playersCheck = playersCheck
      self.getLastMessage = getLastMessage
      self.injectedArgs = []
      super(CheckPlayersCommandTask, self).__init__(discordClient)

   def Start(self, server_id, channel):
      super(CheckPlayersCommandTask, self).Start(server_id, 0, channel)
   
   async def Run(self, server_id, time, channel):
      settingObj = self.settingManager.LoadSettings(channel.guild.id)
      thisGuild = channel.guild
      fullMode = False
      if len(self.injectedArgs) > 0:
         if self.injectedArgs[0] == "full":
            fullMode = True
      usersWithoutAccept = await self.playersCheck.Check(server_id, [
         {'id': settingObj[SettingName.PLAYER_WITHOUT_CHARACTER_ROLE_ID.value], 'channels': [settingObj[SettingName.CHARACTERS_CHANNEL_ID.value]]}
      ], PlayerCheckMethod.JOIN_DATE, 2)
      msg = "Players without characters (from 2 days):\n"
      for user in usersWithoutAccept:
         lastMessage = None
         if fullMode:
            lastMessage = await self.getLastMessage.FindMessageByUser(user, settingObj[SettingName.OFFTOPIC_CATEGORY.value], GetLastMessageMode.CATEGORIES)
         if lastMessage is not None:
            msg = msg + "\n- <@{0}> (last message {1} days ago on <#{2}>)".format(user.id, (datetime.datetime.now() - lastMessage.created_at).days, lastMessage.channel.id)
         else:
            msg = msg + "\n- <@{0}>".format(user.id)
      getIdsFromChannelsInCategories = settingObj[SettingName.CATEGORY_FOR_LOOKING_PLAYERS.value]
      channelsToCheck = []
      for categoryId in getIdsFromChannelsInCategories:
         category = discord.utils.find(lambda c: str(c.id) == categoryId, thisGuild.categories)
         if category is not None:
            for c in category.channels:
               channelsToCheck.append(c.id)
      inactiveUsers = await self.playersCheck.Check(server_id, [
         {'id': settingObj[SettingName.PLAYER_WITH_CHARACTER_ROLE_ID.value], 'channels': channelsToCheck}
      ], PlayerCheckMethod.MESSAGE_ADD, 7)
      msg = msg + "\nPlayers with created character but without any game (from 7 days):"
      for user in inactiveUsers:
         lastMessage = None
         if fullMode:
            lastMessage = await self.getLastMessage.FindMessageByUser(user, settingObj[SettingName.OFFTOPIC_CATEGORY.value], GetLastMessageMode.CATEGORIES)
         if lastMessage is not None:
            msg = msg + "\n- <@{0}> (last message {1} days ago on <#{2}>)".format(user.id, (datetime.datetime.now() - lastMessage.created_at).days, lastMessage.channel.id)
         else:
            msg = msg + "\n- <@{0}>".format(user.id)
      await channel.send(msg)


            
         


