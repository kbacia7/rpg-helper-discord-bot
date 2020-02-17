from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseManager():
    def __init__(self, setting_manager):
        self.setting_manager = setting_manager
        self.session_maker = None
        self.engine = None

    def connect(self):
        settingObj = self.setting_manager.load_global_settings()
        self.engine = create_engine(settingObj['database_url'])
        self.session_maker = sessionmaker(bind=self.engine)

    def create_session(self):
        return self.session_maker()
