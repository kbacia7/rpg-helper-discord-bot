import string
import random
import sched
import time
from client import ExDiscordClient
from commandexecutor import CommandExecutor
from argparser import ArgParser
from mention import Mention
from playerscheck import PlayersCheck
from permission import PermissionChecker
from settingmanager import SettingManager
from tasks.checkplayerstask import CheckPlayersTask
from commands.talk import TalkCommand
from commands.check import CheckCommand
from path import Path
if __name__ == "__main__":
   argParser = ArgParser()
   commandExecutor = CommandExecutor({})
   client = ExDiscordClient(commandExecutor, argParser)
   mention = Mention()
   playersCheck = PlayersCheck(client)
   settingManager = SettingManager()
   permissionChecker = PermissionChecker(settingManager)
   checkPlayersTask = CheckPlayersTask(client, settingManager, playersCheck)
   talkCommand = TalkCommand(client, mention, permissionChecker)
   checkCommand = CheckCommand(client, mention, permissionChecker, playersCheck, settingManager)
   commandsToInject = {
      "talk": talkCommand,
      "check": checkCommand
   }

   settingObj = settingManager.LoadSettings()
   checkPlayersTask.Start()
   commandExecutor.commands = commandsToInject
   client.commandExecutor = commandExecutor
   client.run(settingObj['discordToken'])
