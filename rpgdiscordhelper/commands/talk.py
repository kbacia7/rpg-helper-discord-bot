from .base import BaseCommand
import pytimeparse
import discord
import asyncio


class TalkCommand(BaseCommand):
    async def send_message_in_schedule(self, message, channel, time):
        await asyncio.sleep(time)
        await channel.send(message)

    async def execute(self, member, channel, args):
        if self.permission_checker.is_admin(member) is False:
            return
        if len(args) >= 2:
            channel = self.discord_client.get_channel(
                self.mention.get_int(args[0]))
            if channel is not None:
                time = pytimeparse.parse(args[1])
                if time is not None:
                    msg = " ".join(args[2:])
                    asyncio.ensure_future(
                        self.send_message_in_schedule(msg, channel, time))
                else:
                    msg = " ".join(args[1:])
                    await channel.send(msg)
