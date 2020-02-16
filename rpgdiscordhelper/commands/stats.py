from .base import BaseCommand as baseCommand
import discord
import datetime
from rpgdiscordhelper.modules.playercheckmethod import PlayerCheckMethod
from rpgdiscordhelper.modules.getlastmessagemode import GetLastMessageMode
class StatsCommand(baseCommand):
   def __init__(self, discordClient, mention, permissionChecker, statsTask):
      self.statsTask = statsTask
      super(StatsCommand, self).__init__(discordClient, mention, permissionChecker)

   async def Execute(self, member, args): 
      if self.permissionChecker.IsAdmin(member) is False:
         return 
      self.statsTask.injectedArgs = args
      self.statsTask.Start()
      


         
