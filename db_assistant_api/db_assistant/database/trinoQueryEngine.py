from .trino_connection import trino_connection
from dotenv import load_dotenv

load_dotenv()

class TrinoQueryEngine:
    def __init__(self):
        pass

    def execute_query(self, query: str):
        with trino_connection.connection() as conn:
            if conn is None:
                raise Exception("Not connected to Trino")
            query = """
                SELECT aggregates['close'] AS close_price  
                FROM academy.monk_data_warehouse.fct_daily_prices  
                WHERE ticker = 'AAPL'  
                AND date = DATE '2021-02-17' 
            """
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()

