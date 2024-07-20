import redis
import os

class AppConfig:
        SESSION_TYPE = "redis"
        SESSION_PERMANENT = False
        SESSION_USE_SIGNER = True
        SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
