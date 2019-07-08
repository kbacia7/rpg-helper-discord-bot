class PermissionChecker():
   def __init__(self, settingManager):
      self.settingManager = settingManager
      pass
      
   def IsAdmin(self, member):
      allow = False
      settingsObject = self.settingManager.LoadSettings()
      requiredRole = settingsObject['adminRolesIds'] 
      for role in member.roles:
         if str(role.id) in requiredRole:
            allow = True
            break
      return allow