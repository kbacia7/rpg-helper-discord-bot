class CommandExecutor():
   def __init__(self, commands):
       self.commands = commands
       
   async def Execute(self, commandName, member, data):
       if commandName in self.commands:
           data = [x for x in data if x.strip()]
           await self.commands[commandName].Execute(member, data)