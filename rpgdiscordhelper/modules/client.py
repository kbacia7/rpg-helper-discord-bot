import discord
import datetime
from rpgdiscordhelper.modules.settingname import SettingName

class DiscordClientBase(discord.Client):
    def __init__(self, command_executor, arg_parser, setting_manager):
        self.command_executor = command_executor
        self.arg_parser = arg_parser
        self.setting_manager = setting_manager
        super().__init__()

class ExDiscordClient(DiscordClientBase):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message is not None and message.guild is not None:
           settings = self.setting_manager.load_settings(message.guild.id)
           if len(message.content) <= 0 or message.author == self.user:
              return
           if message.channel.category.id in settings[SettingName.CATEGORY_FOR_LOOKING_PLAYERS.value] and str(message.author.id) in settings['checkedInactiveUsers']:
              del settings['checkedInactiveUsers'][str(message.author.id)]
              settings.update_settings(settings)

           if message.content[0] == '/':
              data = self.arg_parser.parse(message.content)
              await self.command_executor.execute(data[0], message.author, message.channel, data[1:])

    """async def on_member_update(self, before, after):
        beforeRolesIds = [str(r.id) for r in before.roles]
        afterRolesIds = [str(r.id) for r in after.roles]
        settingObj = self.settingManager.LoadSettings()
        playerRole = settingObj[SettingName.PLAYER_WITH_CHARACTER_ROLE_ID.value]
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
        self.settingManager.UpdateSettings(settingObj)"""
