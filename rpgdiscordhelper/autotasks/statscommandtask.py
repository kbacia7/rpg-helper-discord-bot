import discord
from rpgdiscordhelper.modules.playercheckmethod import PlayerCheckMethod
from rpgdiscordhelper.autotasks.base import BaseTask
from rpgdiscordhelper.modules.getlastmessagemode import GetLastMessageMode
from rpgdiscordhelper.modules.settingname import SettingName
import datetime


class StatsCommandTask(BaseTask):
    def __init__(self, discord_client, setting_manager):
        self.setting_manager = setting_manager
        self.args = []
        super(StatsCommandTask, self).__init__(discord_client)

    def start(self, server_id, channel):
        super(StatsCommandTask, self).start(server_id, 0, channel)

    async def run(self, server_id, time, channel):
        details_mode = False
        if len(self.args) > 0:
            if self.args[0] == "details":
                details_mode = True

        guild = channel.guild
        settings = self.setting_manager.load_settings(server_id)
        msg_count_by_channels_ids = {}
        count = 0
        from_date = (datetime.datetime.now() -
                     datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        to_date = datetime.datetime.now().strftime("%Y-%m-%d")
        categories_to_read = settings[SettingName.CATEGORY_FOR_STATS.value]
        channels_to_read = []
        guild = self.discord_client.guilds[0]
        for category_id in categories_to_read:
            category = discord.utils.find(lambda c: str(
                c.id) == category_id, guild.categories)
            for readed_channel in category.channels:
                if str(readed_channel.id) not in (
                        settings[SettingName.IGNORED_CHANNELS_FOR_STATS.value]
                ):
                    channels_to_read.append(str(readed_channel.id))
        for channel_id in channels_to_read:
            readed_channel = discord.utils.find(
                lambda c: c.id == int(channel_id), guild.channels)
            async for m in readed_channel.history(limit=5000).filter(
                lambda msg: msg.created_at + datetime.timedelta(days=7) >=
                    datetime.datetime.now()):
                count += 1
                if details_mode is True:
                    if channel_id not in msg_count_by_channels_ids:
                        msg_count_by_channels_ids[channel_id] = 0
                    msg_count_by_channels_ids[channel_id] += 1
        await channel.send(
            "{0} messages at {1} to {2}".format(
                count, from_date, to_date))
        if details_mode is True:
            message = ""
            sorted_by_messages_count = [
                (k, msg_count_by_channels_ids[k]) for k in sorted(
                    msg_count_by_channels_ids,
                    key=msg_count_by_channels_ids.get,
                    reverse=True)]
            for channel_id, messages_count in sorted_by_messages_count:
                message = "{0}- <#{1}> {2} messages\n".format(
                    message, channel_id, messages_count)
            await channel.send(message)
