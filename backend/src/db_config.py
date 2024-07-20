from dotenv import load_dotenv
import redis
import os

#loads env variables
load_dotenv()

class db_config:
    def __init__(self):
        self.data = {
            'user': os.getenv('user'),
            'password': os.getenv('password'),
            'host': os.getenv('host'),
            'database': os.getenv('DB'),
        }

    def get_config(self):
          return self.data
