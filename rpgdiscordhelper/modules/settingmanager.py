import os
import yaml
from rpgdiscordhelper.modules.path import Path
from rpgdiscordhelper.models.ServerSetting import ServerSetting
from rpgdiscordhelper.modules.settingname import SettingName


class SettingManager():
    def __init__(self, database_manager):
        self.settings = {}
        self.database_manager = database_manager

        self.settings_names = {
            SettingName.ADMIN_ROLE_ID.value: '',
            SettingName.CATEGORY_FOR_LOOKING_PLAYERS.value: '',
            SettingName.CATEGORY_FOR_STATS.value: '',
            SettingName.CHARACTERS_CHANNEL_ID.value: '',
            SettingName.LOGS_CHANNEL_ID.value: '',
            SettingName.MESSAGE_FOR_INACTIVE_PLAYERS.value: '',
            SettingName.MESSAGE_FOR_PLAYERS_WITHOUT_CHARACTER.value: '',
            SettingName.OFFTOPIC_CATEGORY.value: '',
            SettingName.PLAYER_WITH_CHARACTER_ROLE_ID.value: '',
            SettingName.PLAYER_WITHOUT_CHARACTER_ROLE_ID.value: '',
            SettingName.IGNORED_CHANNELS_FOR_STATS.value: '',
            'checkedInactiveUsers': {},
            'checkedUsersWithoutAccept': {}
        }
        pass

    def update_global_settings(self, data):
        with open(Path.SETTINGS.value, 'w', encoding='utf-8') as setting_file:
            yaml.dump(data, setting_file, allow_unicode=True)

    def create_global_settings(self):
        default_yaml_settings = {
            SettingName.DISCORD_TOKEN.value: '',
            SettingName.DATABASE_URL.value: '',
        }
        self.update_global_settings(default_yaml_settings)

    def load_global_settings(self):
        if os.path.exists(Path.SETTINGS.value):
            with open(Path.SETTINGS.value, 'r') as yaml_setting_file:
                return yaml.load(yaml_setting_file, Loader=yaml.FullLoader)
        else:
            self.create_global_settings()
            self.load_global_settings()

    def reload_settings(self, server_id):
        self.settings[server_id] = {}
        session = self.database_manager.create_session()
        settings = session.query(ServerSetting).filter(ServerSetting.name.in_(
            self.settings_names), ServerSetting.server_id == server_id).all()
        for setting in settings:
            if setting.name in self.settings_names:
                if setting.name in self.settings[server_id]:
                    self.settings[server_id][setting.name].append(
                        setting.value)
                else:
                    self.settings[server_id][setting.name] = [setting.value]

    def load_settings(self, server_id):
        if server_id in self.settings:
            return self.settings[server_id]
        else:
            self.reload_settings(server_id)
            return self.load_settings(server_id)
