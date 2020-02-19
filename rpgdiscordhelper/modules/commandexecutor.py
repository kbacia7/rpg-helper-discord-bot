class CommandExecutor():
    def __init__(self, commands):
        self.commands = commands

    async def execute(self, command_name, member, channel, data):
        if command_name in self.commands:
            data = [x for x in data if x.strip()]
            await self.commands[command_name].execute(member, channel, data)
