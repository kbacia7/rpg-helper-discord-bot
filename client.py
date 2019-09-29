import discord
import datetime
class DiscordClientBase(discord.Client):
    def __init__(self, commandExecutor, argparser, settingManager):
        self.commandExecutor = commandExecutor
        self.argparser = argparser
        self.settingManager = settingManager
        super().__init__()

class ExDiscordClient(DiscordClientBase):
    async def on_ready(self):
        activity = discord.Activity(name='graczy przez magiczną kulę', type=discord.ActivityType.watching)
        await self.change_presence(activity=activity)
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        settingObj = self.settingManager.LoadSettings()
        if message is None or len(message.content) <= 0 or message.author == self.user:
           return
        if message.channel.category.id in settingObj['categoriesForLookingInactivePlayers'] and str(message.author.id) in settingObj['checkedInactiveUsers']:
            del settingObj['checkedInactiveUsers'][str(message.author.id)]
            settingObj.UpdateSettings(settingObj)

        if message.content[0] == '/':
           data = self.argparser.Parse(message.content)
           await self.commandExecutor.Execute(data[0], message.author, data[1:])

    async def on_member_update(self, before, after):
        beforeRolesIds = [str(r.id) for r in before.roles]
        afterRolesIds = [str(r.id) for r in after.roles]
        settingObj = self.settingManager.LoadSettings()
        playerRole = settingObj['roleWithPlayersWithCharacter']
        if playerRole not in beforeRolesIds and playerRole in afterRolesIds:
           settingObj = self.settingManager.LoadSettings()
           settingObj['playerFromDate'][str(after.id)] = datetime.datetime.now()
           if str(after.id) in settingObj['playerFromDate']:
              del settingObj['checkedUsersWithoutAccept'][str(after.id)]
           self.settingManager.UpdateSettings(settingObj)

    async def on_member_remove(self, member):
        settingObj = self.settingManager.LoadSettings()
        memberId = str(member.id)
        if memberId in settingObj['checkedInactiveUsers']:
           del settingObj['checkedInactiveUsers'][memberId] 
        if memberId in settingObj['checkedUsersWithoutAccept']:
           del settingObj['checkedUsersWithoutAccept'][memberId]
        if memberId in settingObj['playerFromDate']:
           del settingObj['playerFromDate'][memberId]
        self.settingManager.UpdateSettings(settingObj)
