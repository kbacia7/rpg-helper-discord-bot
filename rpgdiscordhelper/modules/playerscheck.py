import discord
import datetime
from rpgdiscordhelper.modules.playercheckmethod import PlayerCheckMethod
class PlayersCheck():
   def __init__(self, discord_client, setting_manager):
      self.discord_client = discord_client
      self.setting_manager = setting_manager
      pass
         
   async def check(self, server_id, dict_data, mode, arg_for_mode):
       #members = discord.utils.find(lambda m: m.guild.id == server_id, s#self.discord_client.get_all_members()
      roles_ids_to_check = [d['id'] for d in dict_data]
      founded_user_names = []
      loaded_messages = []
      guild = discord.utils.find(lambda g: g.id == server_id, self.discord_client.guilds)
      members = guild.members
      if mode is PlayerCheckMethod.MESSAGE_ADD:
         for channels_ids_to_check in [d['channels'] for d in dict_data]:
            for channel_id in channels_ids_to_check:
               channel = discord.utils.find(lambda c: c.id == channel_id, guild.channels)
               async for m in channel.history(limit=200).filter(lambda msg: msg.created_at + datetime.timedelta(days=arg_for_mode) > datetime.datetime.now()):
                  loaded_messages.append(m)
      for member in members:
         for role in member.roles:
            role_id = str(role.id)
            if role_id in roles_ids_to_check:
               if mode is PlayerCheckMethod.JOIN_DATE:
                  if datetime.datetime.now() > member.joined_at + datetime.timedelta(days=arg_for_mode):
                     founded_user_names.append(member)
               elif mode is PlayerCheckMethod.MESSAGE_ADD:
                  user_join_date = member.joined_at
                  if datetime.datetime.now() > user_join_date + datetime.timedelta(days=arg_for_mode): 
                     message = discord.utils.find(lambda m: m.author == member, loaded_messages)
                     if message is None:
                        founded_user_names.append(member)
      return founded_user_names



                        
      

