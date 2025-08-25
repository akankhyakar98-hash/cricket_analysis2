
import pandas as pd
import os
from sqlalchemy import create_engine

def setup_database():
    """
    Loads cleaned CSV data into an SQLite database with separate tables for each match format.
    """
    
    data_dir = "."  

    # List of your cleaned CSV files
    cleaned_files = [
        "Test_Matches_Combined_cleaned.csv",
        "ODI_Matches_Combined_cleaned.csv",
        "T20_Matches_Combined_cleaned.csv"
    ]

    # Create an SQLite database engine. This will create a file named 'cricket_data.db'
    # in your project directory if it doesn't already exist.
    engine = create_engine('sqlite:///cricket_data.db')
    print("✅ Database engine created. Connecting to 'cricket_data.db'...")

    for file_name in cleaned_files:
        file_path = os.path.join(data_dir, file_name)
        
        # Check if the cleaned file exists
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}. Please run the data cleaning script first.")
            continue

        try:
            # Load the cleaned data from the CSV file into a pandas DataFrame
            df = pd.read_csv(file_path)
            
            # Use the filename to determine the table name (e.g., 'Test_Matches_Combined_cleaned' becomes 'test_matches')
            # The .split('_') gets the parts of the filename, and [:2] takes the first two parts
            table_name = '_'.join(file_name.lower().split('_')[:2])
            
            print(f"\n--- Loading data from {file_name} into the '{table_name}' table ---")
            
            # Insert the DataFrame into the SQL table.
        
            # if_exists='replace' will drop the table and create a new one,
            # which is useful for starting fresh each time.
            df.to_sql(table_name, con=engine, index=False, if_exists='replace')
            print(f"✅ Data from {file_name} successfully inserted into the '{table_name}' table.")

        except Exception as e:
            print(f"An error occurred while processing {file_name}: {e}")

    print("\n🎉 Database setup and data insertion are complete! 'cricket_data.db' is ready for analysis.")

# Run the function to set up the database
if __name__ == "__main__":
    setup_database()
