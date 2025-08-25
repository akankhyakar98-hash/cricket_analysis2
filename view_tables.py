import sqlite3
import pandas as pd


database_file = "cricket_data.db"

def view_tables_and_data():
    
    try:
        
        conn = sqlite3.connect(database_file)
        
    
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            print(f"No tables found in '{database_file}'. Please check if the database was created correctly.")
            return

        print(" Successfully connected to the database. Here are the tables:\n")
        
        
        table_names = [table[0] for table in tables]
        for name in table_names:
            print(f"- {name}")
            
        print("\n--- Showing first 5 rows of each table ---\n")
            
        # Loop through each table and print its first 5 rows
        for table_name in table_names:
            print(f"\n✅ Table: {table_name}")
            
            
            query = f"SELECT * FROM {table_name} LIMIT 5;"
            df = pd.read_sql_query(query, conn)
            
            print(df.to_markdown(index=False)) 
            
            
            print("\nColumn data types:")
            print(df.info())

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except FileNotFoundError:
        print(f"Error: The database file '{database_file}' was not found. Please ensure it is in the same folder.")
    finally:
        
        if conn:
            conn.close()


if __name__ == "__main__":
    view_tables_and_data()
