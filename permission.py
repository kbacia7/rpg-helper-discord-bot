class PermissionChecker():
   def __init__(self):
      pass
      
   def IsAdmin(self, member):
      allow = False
      requiredRole = ['572892451107504157', '573268722777587722']
      for role in member.roles:
         if str(role.id) in requiredRole:
            allow = True
            break
      return allow