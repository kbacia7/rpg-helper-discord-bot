from .base import BaseCommand
import discord
import datetime
from rpgdiscordhelper.modules.playercheckmethod import PlayerCheckMethod
from rpgdiscordhelper.modules.getlastmessagemode import GetLastMessageMode


class CheckCommand(BaseCommand):
    def __init__(
            self, discord_client, mention,
            permission_checker, check_players_task):
        self.check_players_task = check_players_task
        super(CheckCommand, self).__init__(
            discord_client, mention, permission_checker)

    async def execute(self, member, channel, args):
        if self.permission_checker.is_admin(member) is False:
            return
        self.check_players_task.args = args
        self.check_players_task.start(member.guild.id, channel)
