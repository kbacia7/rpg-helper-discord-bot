from rpgdiscordhelper.modules.settingname import SettingName

class PermissionChecker():
   def __init__(self, settingManager):
      self.settingManager = settingManager
      pass
      
   def IsAdmin(self, member):
      allow = False
      settingsObject = self.settingManager.LoadSettings(member.guild.id)
      requiredRole = settingsObject[SettingName.ADMIN_ROLE_ID.value] 
      for role in member.roles:
         if str(role.id) in requiredRole:
            allow = True
            break
      return allow