import string
import random
import sched
import time
from rpgdiscordhelper.modules.client import ExDiscordClient
from rpgdiscordhelper.modules.commandexecutor import CommandExecutor
from rpgdiscordhelper.modules.argparser import ArgParser
from rpgdiscordhelper.modules.mention import Mention
from rpgdiscordhelper.modules.playerscheck import PlayersCheck
from rpgdiscordhelper.modules.permission import PermissionChecker
from rpgdiscordhelper.modules.settingmanager import SettingManager
from rpgdiscordhelper.modules.getlastmessage import GetLastMessage
from rpgdiscordhelper.autotasks.statscommandtask import StatsCommandTask
from rpgdiscordhelper.autotasks.checkplayerstask import CheckPlayersTask
from rpgdiscordhelper.autotasks.checkplayerscommandtask import CheckPlayersCommandTask
from rpgdiscordhelper.commands.talk import TalkCommand
from rpgdiscordhelper.commands.check import CheckCommand
from rpgdiscordhelper.commands.stats import StatsCommand

from rpgdiscordhelper.modules.path import Path
if __name__ == "__main__":
   argParser = ArgParser()
   commandExecutor = CommandExecutor({})
   settingManager = SettingManager()
   client = ExDiscordClient(commandExecutor, argParser, settingManager)
   mention = Mention()
   playersCheck = PlayersCheck(client, settingManager)
   permissionChecker = PermissionChecker(settingManager)
   getLastMessage = GetLastMessage(client)
   checkPlayersTask = CheckPlayersTask(client, settingManager, playersCheck)
   statsCommandTask = StatsCommandTask(client, settingManager)
   checkPlayersCommandTask = CheckPlayersCommandTask(client, settingManager, playersCheck, getLastMessage)
   talkCommand = TalkCommand(client, mention, permissionChecker)
   checkCommand = CheckCommand(client, mention, permissionChecker, checkPlayersCommandTask)
   statsCommand = StatsCommand(client, mention, permissionChecker, statsCommandTask)
   commandsToInject = {
      "talk": talkCommand,
      "check": checkCommand,
      "stats": statsCommand
   }

   settingObj = settingManager.LoadSettings()
   checkPlayersTask.Start()
   commandExecutor.commands = commandsToInject
   client.commandExecutor = commandExecutor
   client.run(settingObj['discordToken'])
