import asyncio


class BaseTask():
    def __init__(self, discord_client):
        self.discord_client = discord_client

    def start(self, server_id, wait_seconds, channel=None):
        asyncio.ensure_future(self.run(server_id, wait_seconds, channel))

    async def run(self, server_id, wait_seconds, channel):
        pass
