import os
import pyodbc
import pandas as pd
from dotenv import load_dotenv

if __name__ == "__main__":

    load_dotenv()

    connection_string = os.getenv("CONNECTION_STRING")

    print(connection_string)

    try:
        conn = pyodbc.connect(connection_string)
        print("Connection successful!")

        ticker = "9432"
        start_date = "2024-01-01"
        end_date = "2024-06-30"

        # ストアドプロシージャを呼び出し、結果をDataFrameに格納
        query = f"EXEC dbo.spGetTradesOnChart @ticker = '{ticker}', @date_from = '{start_date}', @date_to = '{end_date}'"
        df = pd.read_sql(query, conn)

        print(df)

    except pyodbc.Error as e:
        print(f"Error occurred: {e}")

    print("finished.")
