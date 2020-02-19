class BaseCommand():
    def __init__(self, discord_client, mention, permission_checker):
        self.discord_client = discord_client
        self.mention = mention
        self.permission_checker = permission_checker

    async def execute(self, member, channel, args):
        pass
