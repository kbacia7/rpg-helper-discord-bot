class BaseCommand():
   def __init__(self, discordClient, mention, permissionChecker):
      self.discordClient = discordClient
      self.mention = mention
      self.permissionChecker = permissionChecker

   async def Execute(self, args):
      pass
      
