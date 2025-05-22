import psycopg2
from config import Config

class PostgresManager:
    def __init__(self):
        self.conn = psycopg2.connect(**Config.DB_CONFIG)
        
    def __del__(self):
        self.conn.close()
        
    def get_business_data(self, business_id):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM businesses WHERE id = %s", (business_id,))
                result = cursor.fetchone()
                if not result:
                    raise ValueError(f"No business found with ID {business_id}")
                return {
                    "legal_name": result[1],
                    "owner_info": result[2],
                    # dont know the structure of db, dont't know what fields to initialize
                }
        except Exception as e:
            raise RuntimeError(f"Database operation failed: {str(e)}")
