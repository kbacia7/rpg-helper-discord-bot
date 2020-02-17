from rpgdiscordhelper.modules.settingname import SettingName

class PermissionChecker():
   def __init__(self, setting_mnager):
      self.setting_manager = setting_mnager
      pass
      
   def is_admin(self, member):
      allow = False
      settings = self.setting_manager.load_settings(member.guild.id)
      required_role_ids = settings[SettingName.ADMIN_ROLE_ID.value] 
      for role in member.roles:
         if str(role.id) in required_role_ids:
            allow = True
            break
      return allow