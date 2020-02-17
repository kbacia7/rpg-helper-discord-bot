import string
import random
import sched
import time
from rpgdiscordhelper.modules.client import ExDiscordClient
from rpgdiscordhelper.modules.commandexecutor import CommandExecutor
from rpgdiscordhelper.modules.databasemanager import DatabaseManager
from rpgdiscordhelper.modules.argparser import ArgParser
from rpgdiscordhelper.modules.mention import Mention
from rpgdiscordhelper.modules.playerscheck import PlayersCheck
from rpgdiscordhelper.modules.permission import PermissionChecker
from rpgdiscordhelper.modules.settingmanager import SettingManager
from rpgdiscordhelper.modules.lastmessages import LastMessages
from rpgdiscordhelper.autotasks.statscommandtask import StatsCommandTask
from rpgdiscordhelper.autotasks.checkplayerstask import CheckPlayersTask
from rpgdiscordhelper.autotasks.checkplayerscommandtask import CheckPlayersCommandTask
from rpgdiscordhelper.commands.talk import TalkCommand
from rpgdiscordhelper.commands.check import CheckCommand
from rpgdiscordhelper.commands.stats import StatsCommand
from rpgdiscordhelper.modules.path import Path

if __name__ == "__main__":
   args_parser = ArgParser()
   command_executor = CommandExecutor({})
   database_manager = DatabaseManager(None)
   setting_manager = SettingManager(database_manager)
   database_manager.setting_manager = setting_manager
   client = ExDiscordClient(command_executor, args_parser, setting_manager, database_manager)
   mention = Mention()
   players_check = PlayersCheck(client, setting_manager)
   permission_checker = PermissionChecker(setting_manager)
   last_messages = LastMessages(client)
   check_players_task = CheckPlayersTask(client, setting_manager, players_check, database_manager)
   stats_command_task = StatsCommandTask(client, setting_manager)
   check_players_command_task = CheckPlayersCommandTask(client, setting_manager, players_check, last_messages)
   talk_command = TalkCommand(client, mention, permission_checker)
   check_command = CheckCommand(client, mention, permission_checker, check_players_command_task)
   stats_command = StatsCommand(client, mention, permission_checker, stats_command_task)
   commands = {
      "talk": talk_command,
      "check": check_command,
      "stats": stats_command
   }

   global_settings = setting_manager.load_global_settings()
   for g in client.guilds:
      check_players_task.start(g.id)
   command_executor.commands = commands
   client.command_executor = command_executor
   database_manager.connect()
   client.run(global_settings['discord_token'])
