import pandas as pd

def clean_cricket_data(file_path):

    try:
        # 1. Load the data
        df = pd.read_csv(file_path)
        print(f"\n--- Cleaning started for: {file_path} ---")

        # 2. Check for missing values and duplicates
        print("Initial Info:")
        df.info()
        print("\nInitial Missing Values:")
        print(df.isnull().sum())
        
        print("\nInitial Duplicate Rows:")
        print(df.duplicated().sum())

        # Remove duplicates
        df.drop_duplicates(inplace=True)
        print("Duplicates removed.")

        # 3. Correct Data Types
        numeric_cols = ['runs', 'extras', 'total_runs', 'over_number', 'ball_number', 'wicket']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

        # 4. Perform a consistency check on total_runs
        df['total_runs'] = df['runs'] + df['extras']
        print("\nConsistency check on 'total_runs' complete.")

        # Construct the output filename
        output_filename = file_path.replace('.csv', '_cleaned.csv')

        # 5. Save the cleaned DataFrame
        df.to_csv(output_filename, index=False)
        print(f"✅ Cleaning complete. Cleaned data saved to '{output_filename}'.")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Skipping.")
    except Exception as e:
        print(f"An error occurred while cleaning {file_path}: {e}")

# List of files to clean
files_to_clean = [
    "Test_Matches_Combined.csv",
    "ODI_Matches_Combined.csv",
    "T20_Matches_Combined.csv"
]

# Run the cleaning function for each file
for file in files_to_clean:
    clean_cricket_data(file)