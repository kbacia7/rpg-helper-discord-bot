import discord
from rpgdiscordhelper.modules.playercheckmethod import PlayerCheckMethod
from rpgdiscordhelper.autotasks.base import BaseTask
import asyncio
import datetime
from rpgdiscordhelper.modules.settingname import SettingName
from rpgdiscordhelper.models.InactiveUser import InactiveUser
from rpgdiscordhelper.models.UserWithoutCharacter import UserWithoutCharacter


class CheckPlayersTask(BaseTask):
    def __init__(
            self, discord_client,
            setting_manager, players_check, database_manager):
        self.players_check = players_check
        self.setting_manager = setting_manager
        self.database_manager = database_manager
        super(CheckPlayersTask, self).__init__(discord_client)

    def start(self, server_id):
        super(CheckPlayersTask, self).start(server_id, 21600)

    async def run(self, server_id, time, channel):
        while True:
            await asyncio.sleep(time)
            setting = self.setting_manager.load_settings(server_id)
            guild = discord.utils.find(lambda g: g.id == int(
                server_id), self.discord_client.guilds)
            channel_logs = discord.utils.find(lambda c: c.id == int(
                setting[SettingName.LOGS_CHANNEL_ID.value]), guild.channels)

            users_without_character = await self.players_check.check(
                server_id, [
                    {
                        'id': settings[
                            SettingName.PLAYER_WITHOUT_CHARACTER_ROLE_ID.value
                        ],
                        'channels':
                            settings[SettingName.CHARACTERS_CHANNEL_ID.value]
                    }
                ], PlayerCheckMethod.JOIN_DATE, 2)
            categories_to_read = setting[
                SettingName.CATEGORY_FOR_LOOKING_PLAYERS.value
            ]
            channels_to_read = []
            for category_id in categories_to_read:
                category = discord.utils.find(lambda c: str(
                    c.id) == category_id, guild.categories)
                for c in category.channels:
                    channels_to_read.append(c.id)

            inactive_users = await self.players_check.check(server_id, [
                {
                    'id': settings[
                        SettingName.PLAYER_WITH_CHARACTER_ROLE_ID.value
                    ],
                    'channels': channels_to_read}
                ], PlayerCheckMethod.MESSAGE_ADD, 7)
            message_for_players_without_character = setting[
                SettingName.MESSAGE_FOR_PLAYERS_WITHOUT_CHARACTER.value]
            message_for_inactive_users = setting[
                SettingName.MESSAGE_FOR_INACTIVE_PLAYERS.value]
            if len(users_without_character) > 0:
                users_without_character_ids = [
                    str(u.id) for u in users_without_character]
                session = self.database_manager.create_session()
                users_without_character_with_notification = {
                    int(iu.user_id):
                        iu for iu in (
                            session.query(UserWithoutCharacter).filter(
                                UserWithoutCharacter.user_id.in_(
                                    users_without_character_ids
                                ),
                                UserWithoutCharacter.status == 1,
                                UserWithoutCharacter.server_id == str(
                                    server_id
                                )).all()
                        )
                }
                for user in users_without_character:
                    notification_to_send = True
                    now_date = datetime.datetime.now()
                    if user.id in (
                        users_without_character_with_notification
                    ):
                        if users_without_character_with_notification[user.id]
                        .sended_date + datetime.timedelta(days=2) > now_date:
                            users_without_character_with_notification[user.id]
                            .sended_date = now_date
                        else:
                            notification_to_send = False
                    else:
                        new_user = UserWithoutCharacter(user_id=str(
                            user.id
                        ), sended_date=now_date, server_id=server_id, status=1)
                        session.add(new_user)
                    if notification_to_send:
                        await user.send(message_for_players_without_character)
                        await channel_logs.send(
                            (
                                "<@{0}> got reminder at {1} "
                                "that still doesn't have "
                                "created character").format(user.id, now_date)
                            )
                session.commit()

            if len(inactive_users) > 0:
                inactive_users_ids = [str(u.id) for u in inactive_users]
                session = self.database_manager.create_session()
                inactive_users_with_notification = {
                    int(iu.user_id):
                        iu for iu in session.query(InactiveUser).filter(
                            InactiveUser.user_id.in_(inactive_users_ids),
                            InactiveUser.server_id == str(server_id),
                            InactiveUser.status == 1).all()
                }
                for user in inactive_users:
                    notification_to_send = True
                    now_date = datetime.datetime.now()
                    if user.id in inactive_users_with_notification:
                        if inactive_users_with_notification[user.id]
                        .sended_date + datetime.timedelta(days=5) > now_date:
                            inactive_users_with_notification[user.id]
                            .sended_date = now_date
                        else:
                            notification_to_send = False
                    else:
                        new_inactive_user = InactiveUser(
                            user_id=str(user.id), sended_date=now_date,
                            server_id=server_id, status=1)
                        session.add(new_inactive_user)
                    if notification_to_send:
                        await user.send(message_for_inactive_users)
                        await channel_logs.send(
                            (
                                "<@{0}> got reminder at {1} that "
                                "doesn't have any active game from minimum "
                                "5 days"
                            ).format(
                                user.id, now_date.strftime("%Y-%m-%d %H:%M")
                                ))
                session.commit()
