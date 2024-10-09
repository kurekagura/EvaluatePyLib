import os
import pyodbc
from dotenv import load_dotenv

if __name__ == "__main__":

    load_dotenv()

    connection_string = os.getenv("CONNECTION_STRING")

    print(connection_string)

    try:
        conn = pyodbc.connect(connection_string)
        print("Connection successful!")
    except pyodbc.Error as e:
        print(f"Error occurred: {e}")

    print("finished.")
