from dotenv import load_dotenv
import redis
import os

#loads env variables
load_dotenv()

class AppConfig:
        SESSION_TYPE = "redis"
        SECRET_KEY = os.getenv('secret_key')
        SESSION_PERMANENT = False
        SESSION_USE_SIGNER = True
        SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
