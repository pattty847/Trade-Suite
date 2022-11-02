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

        print("Attempting to connect to database.")

        conn = None
        try:

            if not os.path.isdir("data\database"):
                os.makedirs("data\database")

            conn = sqlite3.connect(db_file)
            print("Database connected.")

        except Error as e:
            print(e)

        return conn
