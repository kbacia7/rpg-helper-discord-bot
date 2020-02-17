import discord
import datetime
from rpgdiscordhelper.modules.settingname import SettingName
from rpgdiscordhelper.models.InactiveUser import InactiveUser
from rpgdiscordhelper.models.UserWithoutCharacter import UserWithoutCharacter

class DiscordClientBase(discord.Client):
    def __init__(self, command_executor, arg_parser, setting_manager, database_manager):
        self.command_executor = command_executor
        self.arg_parser = arg_parser
        self.setting_manager = setting_manager
        self.database_manager = database_manager
        super().__init__()

class ExDiscordClient(DiscordClientBase):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message is not None and message.guild is not None:
           settings = self.setting_manager.load_settings(message.guild.id)
           if len(message.content) <= 0 or message.author == self.user:
              return
           if str(message.channel.category.id) in settings[SettingName.CATEGORY_FOR_LOOKING_PLAYERS.value]:
              session = self.database_manager.create_session()
              session.query(InactiveUser).filter(InactiveUser.user_id == str(message.author.id), InactiveUser.server_id == str(message.guild.id)).update({'status': 0}, synchronize_session=False)
              session.commit()

           if message.content[0] == '/':
              data = self.arg_parser.parse(message.content)
              await self.command_executor.execute(data[0], message.author, message.channel, data[1:])

    async def on_member_update(self, before, after):
        before_update_roles_ids = [str(r.id) for r in before.roles]
        after_update_roles_ids = [str(r.id) for r in after.roles]
        settings = self.setting_manager.load_settings(after.guild.id)
        player_with_character_role_id = settings[SettingName.PLAYER_WITH_CHARACTER_ROLE_ID.value]
        if player_with_character_role_id not in before_update_roles_ids and player_with_character_role_id in after_update_roles_ids:
           session = self.database_manager.create_session()
           session.query(UserWithoutCharacter).filter(UserWithoutCharacter.user_id == str(after.id), UserWithoutCharacter.server_id == str(after.guild.id)).update({'status': 0}, synchronize_session=False)
           session.commit()
           

    async def on_member_remove(self, member):
        session = self.database_manager.create_session()
        session.query(UserWithoutCharacter).filter(UserWithoutCharacter.user_id == str(member.id), UserWithoutCharacter.server_id == str(member.guild.id)).update({'status': 0}, synchronize_session=False)
        session.query(InactiveUser).filter(InactiveUser.user_id == str(member.id), InactiveUser.server_id == str(member.guild.id)).update({'status': 0}, synchronize_session=False)
        session.commit()
