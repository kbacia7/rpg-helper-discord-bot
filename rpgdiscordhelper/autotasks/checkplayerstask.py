import discord
from rpgdiscordhelper.modules.playercheckmethod import PlayerCheckMethod
from rpgdiscordhelper.autotasks.base import BaseTask
import asyncio
import datetime
from rpgdiscordhelper.modules.settingname import SettingName

class CheckPlayersTask(BaseTask):
   def __init__(self, discord_client, setting_manager, players_check):
      self.players_check = players_check
      self.setting_manager = setting_manager
      super(CheckPlayersTask, self).__init__(discord_client)

   def start(self, server_id):
      super(CheckPlayersTask, self).start(server_id, 21600)
   
   async def run(self, server_id, time, channel):
      while True:
         await asyncio.sleep(time)
         setting = self.setting_manager.load_settings(server_id)
         guild = discord.utils.find(lambda g: g.id == int(server_id), self.discord_client.guilds)
         channel_logs = discord.utils.find(lambda c: c.id == int(setting[SettingName.LOGS_CHANNEL_ID.value]), guild.channels)

         users_without_character = await self.players_check.check(server_id, [
            {'id': setting[SettingName.PLAYER_WITHOUT_CHARACTER_ROLE_ID.value], 'channels': [setting[SettingName.PLAYER_WITH_CHARACTER_ROLE_ID.value]]}
         ], PlayerCheckMethod.JOIN_DATE, 2)
         categories_to_read = setting[SettingName.CATEGORY_FOR_LOOKING_PLAYERS.value]
         channels_to_read = []
         for category_id in categories_to_read:
            category = discord.utils.find(lambda c: str(c.id) == category_id, guild.categories)
            for c in category.channels:
               channels_to_read.append(c.id)
         
         inactive_users = await self.players_check.Check(server_id, [
            {'id': setting[SettingName.PLAYER_WITH_CHARACTER_ROLE_ID.value], 'channels': channels_to_read}
         ], PlayerCheckMethod.MESSAGE_ADD, 5)
         message_for_players_without_character = setting[SettingName.MESSAGE_FOR_PLAYERS_WITHOUT_CHARACTER.value]
         message_for_inactive_users = setting[SettingName.MESSAGE_FOR_INACTIVE_PLAYERS.value]
         for user in users_without_character:
            if str(user.id) not in setting['checkedUsersWithoutAccept']:
               send_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
               setting['checkedUsersWithoutAccept'][str(user.id)] = send_date
               await user.send(message_for_players_without_character)
               await channel_logs.send("<@{0}> got reminder at {1} that still doesn't have created character".format(user.id, send_date))
         for user in inactive_users:
            if str(user.id) not in setting['checkedInactiveUsers']:
               send_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
               setting['checkedInactiveUsers'][str(user.id)] = send_date
               await user.send(message_for_inactive_users)
               await channel_logs.send("<@{0}> got reminder at {1} that doesn't have any active game from minimum 5 days".format(user.id, send_date))
         self.setting_manager.UpdateSettings(setting)
         


