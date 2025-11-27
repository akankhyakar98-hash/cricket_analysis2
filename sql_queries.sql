create database cricket_analysis_db
Select * from Odi_matches
SELECT Man_Of_Match, COUNT(Man_Of_Match) AS MoM_Awards
FROM odi_matches WHERE Man_Of_Match IS NOT NULL AND Man_Of_Match != 'Unknown'GROUP BY Man_Of_Match
ORDER BY MoM_Awards DESC LIMIT 10;
#top performers from t20
SELECT Man_Of_Match, COUNT(Man_Of_Match) AS MoM_Awards
FROM t20_matches WHERE Man_Of_Match IS NOT NULL AND Man_Of_Match != 'Unknown'
GROUP BY Man_Of_Match ORDER BY MoM_Awards DESC
LIMIT 5;
#3.Team with the highest win percentage in Test cricket
SELECT
    Toss_Winner AS Team_Name,
    COUNT(CASE WHEN Match_Winner = Toss_Winner THEN 1 END) AS Toss_Wins,
    COUNT(*) AS Total_Matches,
    (COUNT(CASE WHEN Match_Winner = Toss_Winner THEN 1 END) * 100.0 / COUNT(*)) AS Win_Percentage_After_Toss_Win
FROM test_matches GROUP BY Team_Name ORDER BY Win_Percentage_After_Toss_Win DESC;
#4.Matches with the Narrowest Margin of Victory
(SELECT Date, Venue, Match_Winner, '1 Run' AS Margin_Description
    FROM odi_matches WHERE Win_By_Runs = 1
)
UNION ALL
( SELECT
        Date,
        Venue,
        Match_Winner,
        '1 Wicket' AS Margin_Description
    FROM
        odi_matches
    WHERE
        Win_By_Wickets = 1
)
UNION ALL
(
    SELECT
        Date,
        Venue,
        Match_Winner,
        '1 Run' AS Margin_Description
    FROM
        t20_matches
    WHERE
        Win_By_Runs = 1
)
UNION ALL
( SELECT Date, Venue, Match_Winner,'1 Wicket' AS Margin_Description 
    FROM t20_matches WHERE Win_By_Wickets = 1)ORDER BY Margin_Description;
# 5.Match Result Distribution by Toss Decision (ODI)
SELECT
    Choose_To,
    COUNT(*) AS Total_Matches,
    SUM(CASE 
        WHEN Match_Winner = Toss_Winner THEN 1 
        ELSE 0 
    END) AS Wins_After_Toss,
    (SUM(CASE 
        WHEN Match_Winner = Toss_Winner THEN 1 
        ELSE 0 
    END) * 100.0 / COUNT(*)) AS Win_Percentage
FROM odi_matches
WHERE Match_Winner IS NOT NULL AND Match_Winner != 'No Result' GROUP BY Choose_To;  
#6.Ranking Teams by Overall Wins
WITH CombinedWins AS ( 
    SELECT Match_Winner AS Team FROM odi_matches WHERE Match_Winner != 'No Result'
    UNION ALL
    
    SELECT Match_Winner AS Team FROM t20_matches WHERE Match_Winner != 'No Result'
    UNION ALL

    SELECT Match_Winner AS Team FROM test_matches WHERE Match_Winner != 'No Result'
)
SELECT Team, COUNT(Team) AS Total_Wins
FROM CombinedWins GROUP BY Team ORDER BY Total_Wins DESC LIMIT 5;  
#7.Identifying Upset Victories(a team won the match but the mom award goes to the loosing side)
SELECT Date, Venue, Match_Winner, Man_Of_Match
FROM odi_matches WHERE Man_Of_Match IS NOT NULL AND Man_Of_Match != 'Unknown'
AND Match_Winner != 'No Result' AND Match_Winner != (
SELECT Toss_Winner FROM odi_matches AS T2 WHERE T2.Man_Of_Match = odi_matches.Man_Of_Match
AND T2.Toss_Winner = odi_matches.Toss_Winner) ORDER BY Date DESC LIMIT 10;
#8.Top 5 Venues by Total Matches Hosted Across All Formats
WITH AllMatches AS (
    SELECT Venue, 'ODI' AS Format FROM odi_matches
    UNION ALL
    SELECT Venue, 'T20' AS Format FROM t20_matches
    UNION ALL
    SELECT Venue, 'Test' AS Format FROM test_matches
)
SELECT
    Venue,
    COUNT(*) AS Total_Matches_Hosted
FROM
    AllMatches
GROUP BY
    Venue
ORDER BY
    Total_Matches_Hosted DESC
LIMIT 5;
#9.Teams That Always Win the Toss But Choose Opposite Decisions
SELECT
    Toss_Winner,
    CONCAT('Decisions Made: ', GROUP_CONCAT(DISTINCT Choose_To)) AS Decisions
FROM
    odi_matches
GROUP BY
    Toss_Winner
HAVING
    COUNT(DISTINCT Choose_To) = 2;
#10.Teams with the Highest Number of Consecutive MoM Awards
WITH PlayerAwards AS (
    SELECT Date, Man_Of_Match AS Player FROM odi_matches WHERE Man_Of_Match IS NOT NULL AND Man_Of_Match != 'Unknown'
    UNION ALL
    SELECT Date, Man_Of_Match AS Player FROM t20_matches WHERE Man_Of_Match IS NOT NULL AND Man_Of_Match != 'Unknown'
    UNION ALL
    SELECT Date, Man_Of_Match AS Player FROM test_matches WHERE Man_Of_Match IS NOT NULL AND Man_Of_Match != 'Unknown'
),
RankedAwards AS (
    SELECT
        Player,
        Date,
        ROW_NUMBER() OVER(ORDER BY Date) AS Match_Sequence_ID
    FROM PlayerAwards
    ORDER BY Date
)
SELECT 
    Player, 
    COUNT(*) AS Total_MoM_Awards
FROM PlayerAwards
GROUP BY Player
ORDER BY Total_MoM_Awards DESC
LIMIT 10;
#11.Self-Joins for Sequential Analysis (Test Matches)
SELECT
    T1.Date AS First_Match_Date,
    T1.Match_Winner AS Team_Name,
    T2.Date AS Second_Match_Date
FROM
    test_matches T1
JOIN
    test_matches T2 ON T1.Match_Winner = T2.Match_Winner
WHERE
    T1.Date < T2.Date
ORDER BY
    T1.Date
LIMIT 10;
#12.Find Pairs of Test Matches Where the Venue Remained the Same:
SELECT
    T1.Venue,
    T1.Date AS Match_1_Date,
    T2.Date AS Match_2_Date
FROM
    test_matches T1
JOIN
    test_matches T2 ON T1.Venue = T2.Venue
WHERE
    T1.Date < T2.Date 
ORDER BY
    T1.Venue, T1.Date
LIMIT 10;
#13. Identify T20 Matches Where the Toss Winner Also Won by a Wickets Margin > 5:
SELECT
    T1.Date,
    T1.Venue,
    T1.Toss_Winner,
    T1.Win_By_Wickets
FROM
    t20_matches T1
WHERE
    T1.Toss_Winner = T1.Match_Winner
    AND T1.Win_By_Wickets > 5;
# 14. Calculate Head-to-Head Win-Loss Record Between Two Specific Teams (e.g., India vs. Australia):
SELECT
    SUM(CASE WHEN Match_Winner = 'India' THEN 1 ELSE 0 END) AS India_Wins,
    SUM(CASE WHEN Match_Winner = 'Australia' THEN 1 ELSE 0 END) AS Australia_Wins,
    COUNT(*) AS Total_Matches
FROM odi_matches WHERE
    (Team_1 = 'India' AND Team_2 = 'Australia') OR (Team_1 = 'Australia' AND Team_2 = 'India')
    AND Match_Winner != 'No Result';   
#15. Find the Most Frequent Match-Up (Teams Playing Each Other Most Often):
WITH Matchups AS (
    SELECT 
        CASE WHEN Team_1 < Team_2 THEN Team_1 ELSE Team_2 END AS Team_A,
        CASE WHEN Team_1 < Team_2 THEN Team_2 ELSE Team_1 END AS Team_B
    FROM odi_matches
)
SELECT
    Team_A || ' vs ' || Team_B AS Match_Up,
    COUNT(*) AS Total_Meetings
FROM
    Matchups
GROUP BY
    Match_Up
ORDER BY
    Total_Meetings DESC
LIMIT 5;    