from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseManager():
    def __init__(self, settingManager):
        self.settingManager = settingManager
        self.sessionMaker = None
        self.engine = None

    def connect(self):
        settingObj = self.settingManager.LoadSettings()
        self.engine = create_engine(settingObj['database_url'])
        self.sessionMaker = sessionmaker(bind=self.engine)

    def create_session(self):
        return self.sessionMaker()