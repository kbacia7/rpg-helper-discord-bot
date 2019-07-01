from commands.base import BaseCommand as baseCommand
import discord
class CheckCommand(baseCommand):
   def __init__(self, discordClient, mention, permissionChecker, playersCheck):
      self.playersCheck = playersCheck
      super(CheckCommand, self).__init__(discordClient, mention, permissionChecker)

   async def Execute(self, member, args): 
      if self.permissionChecker.IsAdmin(member) is False:
         return
      channelToSend = None
      if len(args) <= 0:
         channelToSend = discord.utils.find(lambda c: c.name == "klaudiusz-testing", self.discordClient.get_all_channels())
      else:
         channelToSend = self.discordClient.get_channel(self.mention.getInt(args[0]))
      usersToRemove = await self.playersCheck.Check([{'id': '572897687502848034', 'channels': ['572896095374409730']}], "JOIN_DATE", 2)
      if channelToSend is not None:
         msg = "Przyjezdni bez zaakceptowanej KP od dwóch dni:\n"
         for userId in usersToRemove:
            msg = msg + "\n- <@{0}>".format(userId)
         getIdsFromChannelsInCategories = ['573189641797238795', '573189424897064964', '573189367137566750', '573189223608352779', '573189156717592586', '573100293240258629']
         channelsToCheck = []
         thisGuild = self.discordClient.guilds[0]
         for categoryId in getIdsFromChannelsInCategories:
            category = discord.utils.find(lambda c: str(c.id) == categoryId, thisGuild.categories)
            for channel in category.channels:
               channelsToCheck.append(str(channel.id))
         usersToRemove = await self.playersCheck.Check([{'id': '575301044695728158', 'channels': channelsToCheck}], "MESSAGE_AGO", 7)
         msg = msg + "\n\nGracze bez aktywnej sesji od 7 dni:"
         for userId in usersToRemove:
            msg = msg + "\n- <@{0}>".format(userId)
         msg = msg + "\n\nStwórca nie jest zadowolony..."         
         await channelToSend.send(msg)