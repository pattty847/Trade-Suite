import os
import sqlite3
from sqlite3 import Error

class DB():

    def __init__(self, db_file) -> None:
        self.connection = self.create_connection(db_file)


    def create_connection(self, db_file):
        """ This function will create a database connection to SQLite. 

        Args:
            db_file (str): This is where the database will saved.
        """

        print("Connecting to database...")

        conn = None
        try:

            if not os.path.isdir("data\database"):
                os.makedirs("data\database")

            conn = sqlite3.connect(db_file)
            print("Database connected.")

        except Error as e:
            print(e)

        return conn


    def create_table(self, table):
        """ This will create the tables associated with storing exchange data.
        """
        
        try: 
            c = self.connection.cursor()
            c.execute(table)
        except Error as e:
            print(e)

    
    def create_candlestick_table(self):
        table = """
            CREATE TABLE candlestick (
                “id” INTEGER PRIMARY KEY AUTOINCREMENT,
                “timestamp” DATETIME NOT NULL,
                “open” DECIMAL(12, 6) NOT NULL,
                “high” DECIMAL(12, 6) NOT NULL,
                “low” DECIMAL(12, 6) NOT NULL,
                “close” DECIMAL(12, 6) NOT NULL,
                “volume” DECIMAL(12, 6) NOT NULL
                );
        """

        self.create_table(table)