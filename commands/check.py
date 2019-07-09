from commands.base import BaseCommand as baseCommand
import discord
import datetime
from playercheckmethod import PlayerCheckMethod
from getlastmessagemode import GetLastMessageMode
class CheckCommand(baseCommand):
   def __init__(self, discordClient, mention, permissionChecker, checkPlayersTask):
      self.checkPlayersTask = checkPlayersTask
      super(CheckCommand, self).__init__(discordClient, mention, permissionChecker)

   async def Execute(self, member, args): 
      if self.permissionChecker.IsAdmin(member) is False:
         return 
      self.checkPlayersTask.injectedArgs = args
      self.checkPlayersTask.Start()
      


         
