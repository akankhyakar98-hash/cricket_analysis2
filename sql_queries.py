import sqlite3
import pandas as pd

def run_sql_query(title, query, db_file="cricket_data.db"):
    """
    Connects to an SQLite database, runs a given SQL query, and prints the result.
    
    Args:
        title (str): The title for the query result display.
        query (str): The SQL query string to be executed.
        db_file (str): The name of the database file.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        
        # Use pandas to run the query and store the results in a DataFrame
        result_df = pd.read_sql_query(query, conn)
        
        if result_df.empty:
            print(f"--- {title} ---")
            print("No results found for this query.")
            return

        print(f"\n--- {title} ---")
        print(result_df.to_markdown(index=False))

    except sqlite3.Error as e:
        print(f"SQLite error running '{title}': {e}")
    except FileNotFoundError:
        print(f"Error: The database file '{db_file}' was not found.")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    

    # 1. Top 10 batsmen by total runs in ODIs
    q1 = """
    SELECT
        batter,
        SUM(runs + extras) AS total_runs
    FROM
        odi_matches
    GROUP BY
        batter
    ORDER BY
        total_runs DESC
    LIMIT 10;
    """

    # 2. Leading wicket-takers in T20 matches
    q2 = """
    SELECT
        bowler,
        SUM(wicket) AS total_wickets
    FROM
        t20_matches
    GROUP BY
        bowler
    ORDER BY
        total_wickets DESC
    LIMIT 10;
    """

    # 3. Team with the highest win percentage in Tests
    q3 = """
    WITH TeamMatches AS (
        SELECT team_1 AS team FROM test_matches
        UNION ALL
        SELECT team_2 AS team FROM test_matches
    )
    SELECT
        t1.match_winner AS team,
        COUNT(t1.match_winner) * 100.0 / (SELECT COUNT(*) FROM TeamMatches WHERE team = t1.match_winner) AS win_percentage
    FROM
        test_matches t1
    WHERE
        t1.match_winner != 'No result'
    GROUP BY
        t1.match_winner
    ORDER BY
        win_percentage DESC
    LIMIT 10;
    """

    # 4. Total number of centuries across all match formats
    # Note: This query calculates centuries per player across all formats
    q4 = """
    SELECT
        batter,
        COUNT(*) AS total_centuries
    FROM (
        SELECT
            match_id,
            batter,
            SUM(runs + extras) AS total_runs
        FROM odi_matches
        GROUP BY match_id, batter
        HAVING total_runs >= 100
        UNION ALL
        SELECT
            match_id,
            batter,
            SUM(runs + extras) AS total_runs
        FROM t20_matches
        GROUP BY match_id, batter
        HAVING total_runs >= 100
        UNION ALL
        SELECT
            match_id,
            batter,
            SUM(runs + extras) AS total_runs
        FROM test_matches
        GROUP BY match_id, batter
        HAVING total_runs >= 100
    ) AS all_centuries
    GROUP BY
        batter
    ORDER BY
        total_centuries DESC
    LIMIT 10;
    """

    # 5. Matches with the highest total runs (as a proxy for high-scoring games)
    q5 = """
    SELECT
        match_id,
        SUM(total_runs) AS total_runs_in_match
    FROM
        t20_matches
    GROUP BY
        match_id
    ORDER BY
        total_runs_in_match DESC
    LIMIT 10;
    """
    
    # 6. Top 10 bowlers by wickets in ODI matches
    q6 = """
    SELECT
        bowler,
        SUM(wicket) AS total_wickets
    FROM
        odi_matches
    GROUP BY
        bowler
    ORDER BY
        total_wickets DESC
    LIMIT 10;
    """

    # 7. Top 10 bowlers by wickets in Test matches
    q7 = """
    SELECT
        bowler,
        SUM(wicket) AS total_wickets
    FROM
        test_matches
    GROUP BY
        bowler
    ORDER BY
        total_wickets DESC
    LIMIT 10;
    """
    
    # 8. Team with the highest win percentage in ODIs
    q8 = """
    WITH TeamMatches AS (
        SELECT team_1 AS team FROM odi_matches
        UNION ALL
        SELECT team_2 AS team FROM odi_matches
    )
    SELECT
        t1.match_winner AS team,
        COUNT(t1.match_winner) * 100.0 / (SELECT COUNT(*) FROM TeamMatches WHERE team = t1.match_winner) AS win_percentage
    FROM
        odi_matches t1
    WHERE
        t1.match_winner != 'No result'
    GROUP BY
        t1.match_winner
    ORDER BY
        win_percentage DESC
    LIMIT 10;
    """

    # 9. Top 10 batsmen by total runs in Test matches
    q9 = """
    SELECT
        batter,
        SUM(runs + extras) AS total_runs
    FROM
        test_matches
    GROUP BY
        batter
    ORDER BY
        total_runs DESC
    LIMIT 10;
    """
    
    # 10. Top 10 batsmen by total runs in T20 matches
    q10 = """
    SELECT
        batter,
        SUM(runs + extras) AS total_runs
    FROM
        t20_matches
    GROUP BY
        batter
    ORDER BY
        total_runs DESC
    LIMIT 10;
    """
    
    # 11. Most frequent venue for Test matches
    q11 = """
    SELECT
        venue,
        COUNT(DISTINCT match_id) AS total_matches_played
    FROM
        test_matches
    GROUP BY
        venue
    ORDER BY
        total_matches_played DESC
    LIMIT 10;
    """

    # 12. Most frequent venue for ODI matches
    q12 = """
    SELECT
        venue,
        COUNT(DISTINCT match_id) AS total_matches_played
    FROM
        odi_matches
    GROUP BY
        venue
    ORDER BY
        total_matches_played DESC
    LIMIT 10;
    """

    # 13. Most frequent venue for T20 matches
    q13 = """
    SELECT
        venue,
        COUNT(DISTINCT match_id) AS total_matches_played
    FROM
        t20_matches
    GROUP BY
        venue
    ORDER BY
        total_matches_played DESC
    LIMIT 10;
    """

    # 14. Average total runs per match in each format
    q14 = """
    SELECT
        'Test' AS match_format,
        AVG(total_runs_per_match) AS avg_total_runs
    FROM (
        SELECT match_id, SUM(total_runs) AS total_runs_per_match FROM test_matches GROUP BY match_id
    )
    UNION ALL
    SELECT
        'ODI' AS match_format,
        AVG(total_runs_per_match) AS avg_total_runs
    FROM (
        SELECT match_id, SUM(total_runs) AS total_runs_per_match FROM odi_matches GROUP BY match_id
    )
    UNION ALL
    SELECT
        'T20' AS match_format,
        AVG(total_runs_per_match) AS avg_total_runs
    FROM (
        SELECT match_id, SUM(total_runs) AS total_runs_per_match FROM t20_matches GROUP BY match_id
    );
    """

    # 15. Teams with the most total matches played (across all formats)
    q15 = """
    WITH AllMatches AS (
        SELECT team_1 as team FROM test_matches UNION ALL SELECT team_2 FROM test_matches
        UNION ALL
        SELECT team_1 as team FROM odi_matches UNION ALL SELECT team_2 FROM odi_matches
        UNION ALL
        SELECT team_1 as team FROM t20_matches UNION ALL SELECT team_2 FROM t20_matches
    )
    SELECT
        team,
        COUNT(team) AS total_matches_played
    FROM
        AllMatches
    GROUP BY
        team
    ORDER BY
        total_matches_played DESC
    LIMIT 10;
    """

    # 16. Toss decision breakdown for Test matches
    q16 = """
    SELECT
        toss_decision,
        COUNT(DISTINCT match_id) AS total_matches
    FROM
        test_matches
    GROUP BY
        toss_decision;
    """

    # 17. Toss decision breakdown for ODI matches
    q17 = """
    SELECT
        toss_decision,
        COUNT(DISTINCT match_id) AS total_matches
    FROM
        odi_matches
    GROUP BY
        toss_decision;
    """

    # 18. Toss decision breakdown for T20 matches
    q18 = """
    SELECT
        toss_decision,
        COUNT(DISTINCT match_id) AS total_matches
    FROM
        t20_matches
    GROUP BY
        toss_decision;
    """

    # 19. Matches with the most 'extras' runs
    q19 = """
    SELECT
        match_id,
        SUM(extras) AS total_extras
    FROM
        t20_matches
    GROUP BY
        match_id
    ORDER BY
        total_extras DESC
    LIMIT 10;
    """

    # 20. Top 10 batsmen with the most sixes in ODIs
    q20 = """
    SELECT
        batter,
        COUNT(*) as total_sixes
    FROM
        odi_matches
    WHERE
        runs = 6
    GROUP BY
        batter
    ORDER BY
        total_sixes DESC
    LIMIT 10;
    """

    
    print(" Successfully connected to 'cricket_data.db'.")
    run_sql_query("Top 10 Batsmen by Total Runs in ODIs", q1)
    run_sql_query("Top 10 Wicket-Takers in T20 Matches", q2)
    run_sql_query("Top 10 Teams by Win Percentage in Tests", q3)
    run_sql_query("Top 10 Players by Total Centuries", q4)
    run_sql_query("Top 10 Matches by Total Runs (High-Scoring Games)", q5)
    run_sql_query("Top 10 Wicket-Takers in ODIs", q6)
    run_sql_query("Top 10 Wicket-Takers in Tests", q7)
    run_sql_query("Top 10 Teams by Win Percentage in ODIs", q8)
    run_sql_query("Top 10 Batsmen by Total Runs in Tests", q9)
    run_sql_query("Top 10 Batsmen by Total Runs in T20s", q10)
    run_sql_query("Top 10 Most Frequent Venues for Tests", q11)
    run_sql_query("Top 10 Most Frequent Venues for ODIs", q12)
    run_sql_query("Top 10 Most Frequent Venues for T20s", q13)
    run_sql_query("Average Runs Per Match by Format", q14)
    run_sql_query("Top 10 Teams by Total Matches Played", q15)
    run_sql_query("Toss Decision Breakdown for Tests", q16)
    run_sql_query("Toss Decision Breakdown for ODIs", q17)
    run_sql_query("Toss Decision Breakdown for T20s", q18)
    run_sql_query("Top 10 Matches by Total Extras in T20s", q19)
    run_sql_query("Top 10 Batsmen by Total Sixes in ODIs", q20)

