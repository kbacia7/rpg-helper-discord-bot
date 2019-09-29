import discord
from playercheckmethod import PlayerCheckMethod
from autotasks.base import BaseTask
from getlastmessagemode import GetLastMessageMode
import datetime

class CheckPlayersCommand(BaseTask):
   def __init__(self, discordClient, settingManager, playersCheck, getLastMessage):
      self.settingManager = settingManager
      self.playersCheck = playersCheck
      self.getLastMessage = getLastMessage
      self.injectedArgs = []
      super(CheckPlayersCommand, self).__init__(discordClient)

   def Start(self):
      super(CheckPlayersCommand, self).Start(0)
   
   async def Run(self, time):
      settingObj = self.settingManager.LoadSettings()
      channelToSend = discord.utils.find(lambda c: c.id == int(settingObj['channelToReceiveCommands']), self.discordClient.get_all_channels())
      fullMode = False
      if len(self.injectedArgs) > 0:
         if self.injectedArgs[0] == "full":
            fullMode = True
      usersWithoutAccept = await self.playersCheck.Check([{'id': settingObj['roleWithPlayersWithoutCharacter'], 'channels': [settingObj['channelWithPlayersCharacters']]}], PlayerCheckMethod.JOIN_DATE, 2)
      if channelToSend is not None:
         msg = "Nowoprzybyli bez KP od dwóch dni:\n"
         for user in usersWithoutAccept:
            lastMessage = None
            if fullMode:
               lastMessage = await self.getLastMessage.FindMessageByUser(user, settingObj['offtopicCategories'], GetLastMessageMode.CATEGORIES)
            if lastMessage is not None:
               msg = msg + "\n- <@{0}> (ostatnia wiadomość {1} dni temu na <#{2}>)".format(user.id, (datetime.datetime.now() - lastMessage.created_at).days, lastMessage.channel.id)
            else:
               msg = msg + "\n- <@{0}>".format(user.id)
         getIdsFromChannelsInCategories = settingObj['categoriesForLookingInactivePlayers']
         channelsToCheck = []
         thisGuild = self.discordClient.guilds[0]
         for categoryId in getIdsFromChannelsInCategories:
            category = discord.utils.find(lambda c: str(c.id) == categoryId, thisGuild.categories)
            if category is not None:
               for channel in category.channels:
                  channelsToCheck.append(str(channel.id))
         inactiveUsers = await self.playersCheck.Check([{'id': settingObj['roleWithPlayersWithCharacter'], 'channels': channelsToCheck}], PlayerCheckMethod.MESSAGE_ADD, 7)
         msg = msg + "\n\nGracze bez aktywnej sesji od 7 dni:"
         for user in inactiveUsers:
            lastMessage = None
            if fullMode:
               lastMessage = await self.getLastMessage.FindMessageByUser(user, settingObj['offtopicCategories'], GetLastMessageMode.CATEGORIES)
            if lastMessage is not None:
               msg = msg + "\n- <@{0}> (ostatnia wiadomość {1} dni temu na <#{2}>)".format(user.id, (datetime.datetime.now() - lastMessage.created_at).days, lastMessage.channel.id)
            else:
               msg = msg + "\n- <@{0}>".format(user.id)
         msg = msg + "\n\nStwórca nie jest zadowolony..."         
         await channelToSend.send(msg)


            
         


