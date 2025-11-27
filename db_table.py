import pandas as pd
import os
from sqlalchemy import create_engine, text

# --- CONFIGURE PATHS AND CONNECTION 
DB_USER = 'root'
DB_PASS = '123456789'
DB_HOST = 'localhost'
DB_NAME = 'cricket_analysis_db' 

BASE_DIR = r'C:\Users\Aakankhya\Cricsheet Match Data Analysis'

CLEANED_INPUT_FOLDER = os.path.join(BASE_DIR, 'cleaned_csv')

TABLE_MAPPING = {
    'Test': 'test_matches',
    'ODI': 'odi_matches',
    'T20': 't20_matches',
}

def load_data_to_separate_tables():
    """Connects to MySQL and loads each cleaned CSV into its respective table."""
    try:
        # 1. Establish the Engine and Create the Database
        engine_base = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/")
        with engine_base.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
            conn.commit()

        # Connect to the target database
        engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
        print(f"✅ Database connection established to '{DB_NAME}'.")

    except Exception as e:
        print(f" ERROR: Could not connect to MySQL Server. Ensure it is running and credentials are correct.")
        print(f"Details: {e}")
        return # Exit the function if connection fails

    # 2. Iterate through all cleaned CSV files
    all_files = os.listdir(CLEANED_INPUT_FOLDER)
    
    for file_name in all_files:
        if file_name.endswith('.csv'):
            file_path = os.path.join(CLEANED_INPUT_FOLDER, file_name)
            
            try:
                df = pd.read_csv(file_path)
                
                # Determine the Match Type and target table
                match_type_in_file = df['Match_Type'].iloc[0] 
                target_table = TABLE_MAPPING.get(match_type_in_file, 'unclassified_matches')
                
                # 3. Load Data into the SQL Table
                df.to_sql(
                    name=target_table, 
                    con=engine, 
                    if_exists='replace', 
                    index=False,
                    chunksize=1000
                )
                print(f" Loaded {len(df)} rows from {file_name} into table '{target_table}'.")

            except Exception as e:
                print(f"  ERROR processing {file_name}: {e}")

    print("\n Database loading complete!")

load_data_to_separate_tables()   