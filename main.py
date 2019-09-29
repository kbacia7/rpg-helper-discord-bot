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
from getlastmessage import GetLastMessage
from autotasks.checkplayerstask import CheckPlayersTask
from autotasks.checkplayerscommand import CheckPlayersCommand
from commands.talk import TalkCommand
from commands.check import CheckCommand
from path import Path
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
   checkPlayersCommandTask = CheckPlayersCommand(client, settingManager, playersCheck, getLastMessage)
   talkCommand = TalkCommand(client, mention, permissionChecker)
   checkCommand = CheckCommand(client, mention, permissionChecker, checkPlayersCommandTask)
   commandsToInject = {
      "talk": talkCommand,
      "check": checkCommand
   }

   settingObj = settingManager.LoadSettings()
   checkPlayersTask.Start()
   commandExecutor.commands = commandsToInject
   client.commandExecutor = commandExecutor
   client.run(settingObj['discordToken'])
