import os
import yaml
from path import Path
class SettingManager():
   def __init__(self):
      self.settings = None
      pass
   
   def UpdateSettings(self, obj): 
      with open(Path.SETTINGS.value, 'w', encoding="utf-8") as settingFile:
         yaml.dump(obj, settingFile, allow_unicode=True)
      self.settings = obj

   def CreateSettings(self):
      defaultSettingDict = {
         'discordToken': '', 
         'adminRolesIds': [], 
         "channelLookingForThread": "",
         "checkedPlayers": [],
         "msgForInactiveUsers": "",
         "msgForUsersWithoutCharacter": ""  ,
         "checkedInactiveUsers": {},
         "checkedUsersWithoutAccept": {}
      }
      self.UpdateSettings(defaultSettingDict)
      
   def LoadSettings(self):
      if self.settings is not None:
         return self.settings
      else:
         if os.path.exists(Path.SETTINGS.value):
            with open(Path.SETTINGS.value, 'r') as settingFile:
               self.settings = yaml.load(settingFile, Loader=yaml.FullLoader)
               return self.settings
         else:
            self.CreateSettings()
            self.LoadSettings()
      
