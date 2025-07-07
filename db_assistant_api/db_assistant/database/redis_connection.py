import redis
from dotenv import load_dotenv

load_dotenv()

import os

class RedisConnection:
    def __init__(self):
        self.host = os.getenv("REDIS_HOST")
        self.port = os.getenv("REDIS_PORT")
        self.password = os.getenv("REDIS_PWD")
        self.user_name = os.getenv("REDIS_USER")
        self.__redis_connection = None
    
    def connect(self):
        try:
            self.__redis_connection = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                username=self.user_name,
                decode_responses=True
            )
            self.__redis_connection.ping()
            print("Connected to Redis")
        except Exception as e:
            raise Exception(f"Failed to connect to Redis: {e}")

conn = RedisConnection()
conn.connect()


