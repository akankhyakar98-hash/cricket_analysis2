import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(
    page_title="Cricket Data Analysis Dashboard",
    page_icon="🏏",
    layout="wide"
)

@st.cache_data
def get_data_for_query(query, db_file="cricket_data.db"):
    
    conn = sqlite3.connect(db_file)
    try:
        df = pd.read_sql_query(query, conn)
    finally:
        
        conn.close()
    return df


queries = {
    "Top 10 Batsmen (ODI)": """
        SELECT batter, SUM(runs + extras) AS total_runs
        FROM odi_matches
        GROUP BY batter ORDER BY total_runs DESC LIMIT 10;
    """,
    "Top 10 Bowlers (T20)": """
        SELECT bowler, SUM(wicket) AS total_wickets
        FROM t20_matches
        GROUP BY bowler ORDER BY total_wickets DESC LIMIT 10;
    """,
    "Team Win Percentage (Test)": """
        WITH TeamMatches AS (SELECT team_1 AS team FROM test_matches UNION ALL SELECT team_2 AS team FROM test_matches)
        SELECT
            t1.match_winner AS team,
            COUNT(t1.match_winner) * 100.0 / (SELECT COUNT(*) FROM TeamMatches WHERE team = t1.match_winner) AS win_percentage
        FROM test_matches t1
        WHERE t1.match_winner != 'No result'
        GROUP BY t1.match_winner ORDER BY win_percentage DESC LIMIT 10;
    """,
    "Top 10 Centuries (All Formats)": """
        SELECT
            batter,
            COUNT(*) AS total_centuries
        FROM (
            SELECT match_id, batter, SUM(runs + extras) AS total_runs FROM odi_matches GROUP BY match_id, batter HAVING total_runs >= 100
            UNION ALL
            SELECT match_id, batter, SUM(runs + extras) FROM t20_matches GROUP BY match_id, batter HAVING SUM(runs + extras) >= 100
            UNION ALL
            SELECT match_id, batter, SUM(runs + extras) FROM test_matches GROUP BY match_id, batter HAVING SUM(runs + extras) >= 100
        ) AS all_centuries
        GROUP BY batter ORDER BY total_centuries DESC LIMIT 10;
    """,
    "Average Runs per Match": """
        SELECT 'Test' AS match_format, AVG(total_runs_per_match) AS avg_total_runs FROM (SELECT match_id, SUM(total_runs) AS total_runs_per_match FROM test_matches GROUP BY match_id)
        UNION ALL
        SELECT 'ODI' AS match_format, AVG(total_runs_per_match) FROM (SELECT match_id, SUM(total_runs) AS total_runs_per_match FROM odi_matches GROUP BY match_id)
        UNION ALL
        SELECT 'T20' AS match_format, AVG(total_runs_per_match) FROM (SELECT match_id, SUM(total_runs) AS total_runs_per_match FROM t20_matches GROUP BY match_id);
    """,
    "ODI Toss Decisions": """
        SELECT toss_decision, COUNT(DISTINCT match_id) AS total_matches
        FROM odi_matches
        GROUP BY toss_decision;
    """,
    "Highest-Scoring T20 Matches": """
        SELECT match_id, SUM(total_runs) AS total_runs_in_match FROM t20_matches
        GROUP BY match_id ORDER BY total_runs_in_match DESC LIMIT 10;
    """,
    "Most Frequent Venues (ODI)": """
        SELECT venue, COUNT(DISTINCT match_id) AS total_matches_played FROM odi_matches
        GROUP BY venue ORDER BY total_matches_played DESC LIMIT 10;
    """,
    "Top 10 Teams by Matches Played": """
        WITH AllMatches AS (
            SELECT team_1 as team FROM test_matches UNION ALL SELECT team_2 FROM test_matches
            UNION ALL
            SELECT team_1 as team FROM odi_matches UNION ALL SELECT team_2 FROM odi_matches
            UNION ALL
            SELECT team_1 as team FROM t20_matches UNION ALL SELECT team_2 FROM t20_matches
        )
        SELECT team, COUNT(team) AS total_matches_played FROM AllMatches
        GROUP BY team ORDER BY total_matches_played DESC LIMIT 10;
    """,
    "Top 10 Batsmen with Most Sixes (ODI)": """
        SELECT batter, COUNT(*) as total_sixes FROM odi_matches
        WHERE runs = 6 GROUP BY batter ORDER BY total_sixes DESC LIMIT 10;
    """
}


def create_dashboard():
    st.title("🏏 Cricket Data Analytics")
    st.markdown("### Interactive Dashboard for Cricsheet Data")
    st.markdown("---")

    
    st.sidebar.header("Dashboard Sections")
    options = ["Player Performance", "Team & Match Analysis"]
    choice = st.sidebar.radio("Go to", options)
    
    # Player Performance 
    if choice == "Player Performance":
        st.header("Player Performance Trends")
        st.markdown("Analyze top performers across different formats.")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Top 10 Batsmen (ODI)")
            df_batsmen = get_data_for_query(queries["Top 10 Batsmen (ODI)"])
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x="total_runs", y="batter", data=df_batsmen, ax=ax, palette="viridis", hue="batter", legend=False)
            ax.set_xlabel("Total Runs")
            ax.set_ylabel("Batsman")
            ax.bar_label(ax.containers[0], fmt='%.0f')
            st.pyplot(fig)

        with col2:
            st.subheader("Top 10 Bowlers (T20)")
            df_bowlers = get_data_for_query(queries["Top 10 Bowlers (T20)"])
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x="total_wickets", y="bowler", data=df_bowlers, ax=ax, palette="GnBu_d", hue="bowler", legend=False)
            ax.set_xlabel("Total Wickets")
            ax.set_ylabel("Bowler")
            ax.bar_label(ax.containers[0], fmt='%.0f')
            st.pyplot(fig)

        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Players with Most Centuries")
            df_centuries = get_data_for_query(queries["Top 10 Centuries (All Formats)"])
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.barplot(x="total_centuries", y="batter", data=df_centuries, ax=ax, palette="coolwarm", hue="batter", legend=False)
            ax.set_xlabel("Number of Centuries")
            ax.set_ylabel("Player")
            ax.bar_label(ax.containers[0], fmt='%.0f')
            st.pyplot(fig)
        
        with col4:
            st.subheader("Top 10 Batsmen with Most Sixes (ODI)")
            df_sixes = get_data_for_query(queries["Top 10 Batsmen with Most Sixes (ODI)"])
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.barplot(x="total_sixes", y="batter", data=df_sixes, ax=ax, palette="husl", hue="batter", legend=False)
            ax.set_xlabel("Total Sixes")
            ax.set_ylabel("Batsman")
            ax.bar_label(ax.containers[0], fmt='%.0f')
            st.pyplot(fig)

    # Team & Match Analysis 
    elif choice == "Team & Match Analysis":
        st.header("Team and Match Outcome Analysis")
        st.markdown("Explore team performance and key match statistics.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Team Win Percentage (Test Matches)")
            df_win_rate = get_data_for_query(queries["Team Win Percentage (Test)"])
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.barplot(x="win_percentage", y="team", data=df_win_rate, ax=ax, palette="YlOrBr", hue="team", legend=False)
            ax.set_xlabel("Win Percentage (%)")
            ax.set_ylabel("Team")
            ax.bar_label(ax.containers[0], fmt='%.1f%%')
            st.pyplot(fig)
        
        with col2:
            st.subheader("ODI Toss Decision Breakdown")
            df_toss = get_data_for_query(queries["ODI Toss Decisions"])
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(df_toss['total_matches'], labels=df_toss['toss_decision'], autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
            ax.set_title("ODI Toss Decision Breakdown", fontsize=16, fontweight='bold')
            st.pyplot(fig)
        
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Average Runs per Match by Format")
            df_avg_runs = get_data_for_query(queries["Average Runs per Match"])
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.barplot(x="match_format", y="avg_total_runs", data=df_avg_runs, ax=ax, palette="tab10", hue="match_format", legend=False)
            ax.set_xlabel("Match Format")
            ax.set_ylabel("Average Total Runs")
            ax.bar_label(ax.containers[0], fmt='%.0f')
            st.pyplot(fig)
        
        with col4:
            st.subheader("Top 10 Teams by Matches Played")
            df_teams = get_data_for_query(queries["Top 10 Teams by Matches Played"])
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.barplot(x="total_matches_played", y="team", data=df_teams, ax=ax, palette="Paired", hue="team", legend=False)
            ax.set_xlabel("Total Matches")
            ax.set_ylabel("Team")
            ax.bar_label(ax.containers[0], fmt='%.0f')
            st.pyplot(fig)
        
        col5, col6 = st.columns(2)
        with col5:
            st.subheader("Highest-Scoring T20 Matches")
            df_high_score_t20 = get_data_for_query(queries["Highest-Scoring T20 Matches"])
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.barplot(x="total_runs_in_match", y="match_id", data=df_high_score_t20, ax=ax, palette="plasma", hue="match_id", legend=False)
            ax.set_xlabel("Total Runs in Match")
            ax.set_ylabel("Match ID")
            ax.bar_label(ax.containers[0], fmt='%.0f')
            st.pyplot(fig)

        with col6:
            st.subheader("Most Frequent Venues (ODI)")
            df_venues_odi = get_data_for_query(queries["Most Frequent Venues (ODI)"])
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.barplot(x="total_matches_played", y="venue", data=df_venues_odi, ax=ax, palette="Greens_d", hue="venue", legend=False)
            ax.set_xlabel("Number of Matches")
            ax.set_ylabel("Venue")
            ax.bar_label(ax.containers[0], fmt='%.0f')
            st.pyplot(fig)


if __name__ == "__main__":
    create_dashboard()
