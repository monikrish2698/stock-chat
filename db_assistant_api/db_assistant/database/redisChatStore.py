from database.redis_connection import conn


class RedisChatStore:
    def __init__(self, conn):
        self.__redis_connection = conn
    
    def get_chat_history(self, session_id: str):
        pass

    def save_chat(self, session_id: str, chat: str):
        pass

    
        