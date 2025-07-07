from .trino_connection import trino_connection
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

class TrinoQueryEngine:
    def __init__(self):
        pass

    def execute_query(self, query: str):
        try:
            with trino_connection.connection() as conn:
                if conn is None:
                    raise Exception("Not connected to Trino")
                cursor = conn.cursor()
                cursor.execute(query)
                rows = cursor.fetchall()
                cols = [col[0] for col in cursor.description]

                return pd.DataFrame(rows, columns=cols)
        except Exception as e:
            return pd.DataFrame({"error": ["Unable to process data. Can you try again?"]})

