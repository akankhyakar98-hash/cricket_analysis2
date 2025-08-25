import os
import json 
import pandas as pd


folder_path = "json-data"

# Lists to store structured data
matches_list = []
deliveries_list = []

print("Processing all JSON files...")
# Loop through all JSON files in the specified folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):  # Process only JSON files
        file_path = os.path.join(folder_path, filename)

        # Generate match_id from file name (remove .json extension)
        match_id = filename.replace(".json", "")

        # Load JSON file
        try:
            with open(file_path, "r") as file:
                match_data = json.load(file)
        except json.JSONDecodeError:
            print(f"Skipping '{filename}' due to a JSON decoding error.")
            continue

        # Extract Match Metadata
        match_info = match_data.get("info", {})
        match_type = match_info.get("match_type", "Unknown")

        # Process all three match types
        if match_type in ["T20", "ODI", "Test"]:
            venue = match_info.get("venue", "Unknown")
            teams = match_info.get("teams", ["Unknown", "Unknown"])
            toss_winner = match_info.get("toss", {}).get("winner", "Unknown")
            toss_decision = match_info.get("toss", {}).get("decision", "Unknown")
            match_winner = match_info.get("outcome", {}).get("winner", "Unknown")

            matches_list.append({
                "match_id": match_id,
                "venue": venue,
                "team_1": teams[0] if len(teams) > 0 else "Unknown",
                "team_2": teams[1] if len(teams) > 1 else "Unknown",
                "match_type": match_type,
                "toss_winner": toss_winner,
                "toss_decision": toss_decision,
                "match_winner": match_winner
            })
            
            # Extract Deliveries Data
            for inning in match_data.get("innings", []):
                batting_team = inning.get("team", "Unknown")

                for over_data in inning.get("overs", []):
                    over_number = int(over_data.get("over", 0))

                    for delivery in over_data.get("deliveries", []):
                        ball_number = int(delivery.get("ball", 0))
                        
                        deliveries_list.append({
                            "match_id": match_id,
                            "batting_team": batting_team,
                            "over_number": over_number,
                            "ball_number": ball_number,
                            "batter": delivery.get("batter", "Unknown"),
                            "bowler": delivery.get("bowler", "Unknown"),
                            "runs": delivery.get("runs", {}).get("batter", 0),
                            "extras": delivery.get("runs", {}).get("extras", 0),
                            "total_runs": delivery.get("runs", {}).get("total", 0),
                            "wicket": 1 if "wickets" in delivery else 0
                        })

# Convert the master lists to DataFrames
matches_df = pd.DataFrame(matches_list)
deliveries_df = pd.DataFrame(deliveries_list)


# Filter for Test matches
test_matches_df = matches_df[matches_df['match_type'] == 'Test']
test_deliveries_df = deliveries_df[deliveries_df['match_id'].isin(test_matches_df['match_id'])]
df_test = pd.merge(test_matches_df, test_deliveries_df, on='match_id')
df_test.to_csv("Test_Matches_Combined.csv", index=False)
print("✅ Test match data saved to 'Test_Matches_Combined.csv'!")

# Filter for ODI matches
odi_matches_df = matches_df[matches_df['match_type'] == 'ODI']
odi_deliveries_df = deliveries_df[deliveries_df['match_id'].isin(odi_matches_df['match_id'])]
df_odi = pd.merge(odi_matches_df, odi_deliveries_df, on='match_id')
df_odi.to_csv("ODI_Matches_Combined.csv", index=False)
print("✅ ODI match data saved to 'ODI_Matches_Combined.csv'!")

# Filter for T20 matches
t20_matches_df = matches_df[matches_df['match_type'] == 'T20']
t20_deliveries_df = deliveries_df[deliveries_df['match_id'].isin(t20_matches_df['match_id'])]
df_t20 = pd.merge(t20_matches_df, t20_deliveries_df, on='match_id')
df_t20.to_csv("T20_Matches_Combined.csv", index=False)
print("✅ T20 match data saved to 'T20_Matches_Combined.csv'!")