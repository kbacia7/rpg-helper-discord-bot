import discord
from playercheckmethod import PlayerCheckMethod
from autotasks.base import BaseTask
import asyncio
import datetime
class RemoveLookingForThreadMessages(BaseTask):
   def __init__(self, discordClient, settingManager):
      self.settingManager = settingManager
      super(RemoveLookingForThreadMessages, self).__init__(discordClient)

   def Start(self):
      super(RemoveLookingForThreadMessages, self).Start(21600)
   
   async def Run(self, time):
      while True:
         await asyncio.sleep(time)
         settingObj = self.settingManager.LoadSettings()
         channelForLookingThread = discord.utils.find(lambda c: c.id == int(settingObj['channelLookingForThread']), self.discordClient.get_all_channels()) 
         channelToSendLog = discord.utils.find(lambda c: c.name == "logi", self.discordClient.get_all_channels())
         msgForRemovedMessage = settingObj['msgForRemovedLookingThreadMessage']
         getNotification = []
         async for m in channelForLookingThread.history(limit=200).filter(lambda msg:  m.pinned is False and datetime.datetime.now() > msg.created_at + datetime.timedelta(days=3)):
            author = m.author
            if str(author.id) not in getNotification:
               author.send(msgForRemovedMessage)
               getNotification.append(str(author.id))
               await m.delete()
               await channelToSendLog.send("Użytkownikowi <@{0}> wygasła wiadomość na <#{1}> dnia {2} i otrzymał powiadomienie".format(author.id, settingObj['channelLookingForThread'], datetime.datetime.now()))

            
         


