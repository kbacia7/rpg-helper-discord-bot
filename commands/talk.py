from commands.base import BaseCommand as baseCommand
import pytimeparse
import discord
import asyncio

class TalkCommand(baseCommand):
   async def SendMessageInSchedule(self, message, channel, time):
      await asyncio.sleep(time)
      await channel.send(message)

   async def Execute(self, member, args): 
      if self.permissionChecker.IsAdmin(member) is False:
         return
      if len(args) >= 2:
         channel = self.discordClient.get_channel(self.mention.getInt(args[0]))
         if channel is not None:
            isTimeGiven = pytimeparse.parse(args[1])
            if isTimeGiven is not None:
               msg = " ".join(args[2:])
               asyncio.ensure_future(self.SendMessageInSchedule(msg, channel, isTimeGiven))
            else:
               msg = " ".join(args[1:])
               await channel.send(msg)