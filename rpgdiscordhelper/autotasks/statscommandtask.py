import discord
from rpgdiscordhelper.modules.playercheckmethod import PlayerCheckMethod
from rpgdiscordhelper.autotasks.base import BaseTask
from rpgdiscordhelper.modules.getlastmessagemode import GetLastMessageMode
import datetime

class StatsCommandTask(BaseTask):
   def __init__(self, discordClient, settingManager):
      self.settingManager = settingManager
      self.injectedArgs = []
      super(StatsCommandTask, self).__init__(discordClient)

   def Start(self):
      super(StatsCommandTask, self).Start(0)
   
   async def Run(self, time):
      fullMode = False
      if len(self.injectedArgs) > 0:
         if self.injectedArgs[0] == "full":
            fullMode = True
      settingObj = self.settingManager.LoadSettings()
      channelToSend = discord.utils.find(lambda c: c.id == int(settingObj['channelToReceiveCommands']), self.discordClient.get_all_channels())
      groupedByChannels = {}
      count = 0
      fromDate = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
      toData =  datetime.datetime.now().strftime("%Y-%m-%d")
      getIdsFromChannelsInCategories = settingObj['categoriesForStats']
      channelsToCheck = []
      thisGuild = self.discordClient.guilds[0]
      for categoryId in getIdsFromChannelsInCategories:
         category = discord.utils.find(lambda c: str(c.id) == categoryId, thisGuild.categories)
         for channel in category.channels:
            if str(channel.id) not in settingObj['ignoredChannelsForStats']:
               channelsToCheck.append(str(channel.id))
      for channelId in channelsToCheck:
         channel = discord.utils.find(lambda c: c.id == int(channelId), self.discordClient.get_all_channels())
         async for m in channel.history(limit=5000).filter(lambda msg: msg.created_at + datetime.timedelta(days=7) >= datetime.datetime.now()):
            count += 1
            if fullMode is True:
               channelGroupKey = str(m.channel.id)
               if channelGroupKey not in groupedByChannels:
                  groupedByChannels[channelGroupKey] = 0
               groupedByChannels[channelGroupKey] += 1
      await channelToSend.send("W sumie {0} wiadomości od {1} do {2}".format(count, fromDate, toData))
      if fullMode is True:
         finalMsg = ""
         groupedByChannelsSorted = [(k, groupedByChannels[k]) for k in sorted(groupedByChannels, key=groupedByChannels.get, reverse=True)]
         for channelId, messagesCount in groupedByChannelsSorted:
            finalMsg = "{0}- <#{1}> {2} wiadomości\n".format(finalMsg, channelId, messagesCount)
         await channelToSend.send(finalMsg)
