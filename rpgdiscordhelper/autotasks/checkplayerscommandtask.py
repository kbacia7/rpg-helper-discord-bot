import discord
from rpgdiscordhelper.modules.playercheckmethod import PlayerCheckMethod
from rpgdiscordhelper.autotasks.base import BaseTask
from rpgdiscordhelper.modules.getlastmessagemode import GetLastMessageMode
from rpgdiscordhelper.modules.settingname import SettingName
import datetime


class CheckPlayersCommandTask(BaseTask):
    def __init__(
            self, discord_client, setting_manager,
            players_check, last_messages):
        self.setting_manager = setting_manager
        self.players_check = players_check
        self.last_messages = last_messages
        self.args = []
        super(CheckPlayersCommandTask, self).__init__(discord_client)

    def start(self, server_id, channel):
        super(CheckPlayersCommandTask, self).start(server_id, 0, channel)

    async def run(self, server_id, time, channel):
        settings = self.setting_manager.load_settings(channel.guild.id)
        guild = channel.guild
        details_mode = False
        if len(self.args) > 0:
            if self.args[0] == "details":
                details_mode = True
        users_without_character = await self.players_check.check(server_id, [
            {
                'id': settings[
                    SettingName.PLAYER_WITHOUT_CHARACTER_ROLE_ID.value],
                'channels': settings[SettingName.CHARACTERS_CHANNEL_ID.value]
            }
        ], PlayerCheckMethod.JOIN_DATE, 2)
        message = "Players without characters (from 2 days):\n"
        for user in users_without_character:
            last_message = None
            if details_mode:
                last_message = await self.last_messages.find_message_by_user(
                    guild.id, user, settings[SettingName.OFFTOPIC_CATEGORY.value],
                    GetLastMessageMode.CATEGORIES)
            if last_message is not None:
                message = message + (
                    "\n- <@{0}> (last message {1} days ago on <#{2}>)".format(
                        user.id,
                        (
                            datetime.datetime.now() - last_message.created_at
                        ).days,
                        last_message.channel.id))
            else:
                message = message + "\n- <@{0}>".format(user.id)
        categories_to_read = settings[
            SettingName.CATEGORY_FOR_LOOKING_PLAYERS.value]
        channels_to_read = []
        for category_id in categories_to_read:
            category = discord.utils.find(lambda c: str(
                c.id) == category_id, guild.categories)
            if category is not None:
                for c in category.channels:
                    channels_to_read.append(c.id)
        inactive_users = await self.players_check.check(server_id, [
            {'id': settings[SettingName.PLAYER_WITH_CHARACTER_ROLE_ID.value],
                'channels': channels_to_read}
        ], PlayerCheckMethod.MESSAGE_ADD, 7)
        message = message + (
            "Players with created character "
            "but without any game (from 7 days):"
        )
        for user in inactive_users:
            last_message = None
            if details_mode:
                last_message = await self.last_messages.find_message_by_user(
                    guild.id user, settings[SettingName.OFFTOPIC_CATEGORY.value],
                    GetLastMessageMode.CATEGORIES)
            if last_message is not None:
                message = message + """
                - <@{0}> (last message {1} days ago on <#{2}>)""".format(
                    user.id,
                    (datetime.datetime.now() - last_message.created_at).days,
                    last_message.channel.id)
            else:
                message = message + "\n- <@{0}>".format(user.id)
        await channel.send(message)
