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

from commands.talk import TalkCommand
from commands.check import CheckCommand

argParser = ArgParser()
commandExecutor = CommandExecutor({})
client = ExDiscordClient(commandExecutor, argParser)
mention = Mention()
playersCheck = PlayersCheck(client)
permissionChecker = PermissionChecker()

talkCommand = TalkCommand(client, mention, permissionChecker)
checkCommand = CheckCommand(client, mention, permissionChecker, playersCheck)
commandsToInject = {
   "talk": talkCommand,
   "check": checkCommand
}
commandExecutor.commands = commandsToInject
client.commandExecutor = commandExecutor
client.run('<YOUR_TOKEN_HERE>')
