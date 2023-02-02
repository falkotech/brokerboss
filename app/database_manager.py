import logging
from pymongo import MongoClient

class DatabaseManager:

    def __init__(self):
        pass
        
        

    def connect_to_database(self, connection_string):
        try:
            max_srv_sel_delay = 5000 # 5s maximum server selection delay
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=max_srv_sel_delay)
            self.db = self.client.brokerboss
            # Create collections if they don't exist
            collection_names = self.db.list_collection_names()
            # Admin collection
            if "admins" not in collection_names:
                self.admin_collection = self.db.create_collection("admins")
            else:
                self.admin_collection = self.db["admins"]
            if "settings" not in collection_names:
                self.settings_collection = self.db.create_collection("settings")
            else:
                self.settings_collection = self.db["settings"]
            logging.info("Connected to database")
            return True
        except Exception as e:
            logging.error(f"Could not connect to database: {e}, Connection string: {connection_string}")
            return False

    def load_general_settings(self):
        try:
            settings = self.settings_collection.find_one({"_id": "general_settings"})
            return settings
        except Exception as e:
            logging.error(f"Could not load general settings: {e}, Type: {type(e)}")
            return None
    
    def save_general_settings(self, settings):
        try:
            result = self.settings_collection.find_one_and_replace({"_id": "general_settings"}, settings, upsert=True)
            return True
        except Exception as e:
            logging.error(f"Could not save general settings: {e}, Type: {type(e)}")
            return False