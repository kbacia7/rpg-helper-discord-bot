import asyncio
class BaseTask():
   def __init__(self, discordClient):
      self.discordClient = discordClient
   
   def Start(self, server_id, waitSeconds, channel=None):
      asyncio.ensure_future(self.Run(server_id, waitSeconds, channel)) 
         
   async def Run(self, server_id, waitSeconds, channel):
      pass
