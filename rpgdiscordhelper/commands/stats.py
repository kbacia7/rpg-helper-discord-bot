from .base import BaseCommand
import discord
import datetime
from rpgdiscordhelper.modules.playercheckmethod import PlayerCheckMethod
from rpgdiscordhelper.modules.getlastmessagemode import GetLastMessageMode


class StatsCommand(BaseCommand):
    def __init__(
            self, discord_client, mention,
            permission_checker, stats_task):
        self.stats_task = stats_task
        super(StatsCommand, self).__init__(
            discord_client, mention, permission_checker)

    async def execute(self, member, channel, args):
        if self.permission_checker.is_admin(member) is False:
            return
        self.stats_task.args = args
        self.stats_task.start(member.guild.id, channel)
