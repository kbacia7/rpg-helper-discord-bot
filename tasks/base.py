import asyncio
class BaseTask():
   def __init__(self, discordClient):
      self.discordClient = discordClient
   
   def Start(self, waitSeconds):
      asyncio.ensure_future(self.Run(waitSeconds)) 
         
   async def Run(self, waitSeconds):
      pass
