import discord
from playercheckmethod import PlayerCheckMethod
from autotasks.base import BaseTask
from getlastmessagemode import GetLastMessageMode
import datetime

class CheckPlayersCommand(BaseTask):
   def __init__(self, discordClient, settingManager, playersCheck, getLastMessage):
      self.settingManager = settingManager
      self.playersCheck = playersCheck
      self.settingManager = settingManager
      self.getLastMessage = getLastMessage
      self.injectedArgs = []
      super(CheckPlayersCommand, self).__init__(discordClient)

   def Start(self):
      super(CheckPlayersCommand, self).Start(0)
   
   async def Run(self, time):
      channelToSend = discord.utils.find(lambda c: c.name == "klaudiusz-testing", self.discordClient.get_all_channels())
      fullMode = False
      if len(self.injectedArgs) > 0:
         if self.injectedArgs[0] == "full":
            fullMode = True
      usersWithoutAccept = await self.playersCheck.Check([{'id': '572897687502848034', 'channels': ['572896095374409730']}], PlayerCheckMethod.JOIN_DATE, 2)
      if channelToSend is not None:
         settingObj = self.settingManager.LoadSettings()
         msg = "Przyjezdni bez KP od dwóch dni:\n"
         for user in usersWithoutAccept:
            lastMessage = None
            if fullMode:
               lastMessage = await self.getLastMessage.FindMessageByUser(user, ["572893870766030898", "572894344080785446", "572895747956277279"], GetLastMessageMode.CATEGORIES)
            if lastMessage is not None:
               msg = msg + "\n- <@{0}> (ostatnia wiadomość {1} dni temu na <#{2}>)".format(user.id, (datetime.datetime.now() - lastMessage.created_at).days, lastMessage.channel.id)
            else:
               msg = msg + "\n- <@{0}>".format(user.id)
         getIdsFromChannelsInCategories = ['573189641797238795', '573189424897064964', '573189367137566750', '573189223608352779', '573189156717592586', '573100293240258629']
         channelsToCheck = []
         thisGuild = self.discordClient.guilds[0]
         for categoryId in getIdsFromChannelsInCategories:
            category = discord.utils.find(lambda c: str(c.id) == categoryId, thisGuild.categories)
            for channel in category.channels:
               channelsToCheck.append(str(channel.id))
         inactiveUsers = await self.playersCheck.Check([{'id': '575301044695728158', 'channels': channelsToCheck}], PlayerCheckMethod.MESSAGE_ADD, 7)
         msg = msg + "\n\nGracze bez aktywnej sesji od 7 dni:"
         for user in inactiveUsers:
            lastMessage = None
            if fullMode:
               lastMessage = await self.getLastMessage.FindMessageByUser(user, ["572893870766030898", "572894344080785446", "572895747956277279"], GetLastMessageMode.CATEGORIES)
            if lastMessage is not None:
               msg = msg + "\n- <@{0}> (ostatnia wiadomość {1} dni temu na <#{2}>)".format(user.id, (datetime.datetime.now() - lastMessage.created_at).days, lastMessage.channel.id)
            else:
               msg = msg + "\n- <@{0}>".format(user.id)
         msg = msg + "\n\nStwórca nie jest zadowolony..."         
         await channelToSend.send(msg)


            
         


