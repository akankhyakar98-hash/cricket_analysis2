# Cricket-Match-Data-Analysis
This project focuses on a comprehensive data analysis of cricket matches, from manual data scraping to interactive visualization. It's a great way to showcase skills in data acquisition, processing, database management, and dashboard creation.

# Cricket Match Data Analysis


##  Project Overview
The primary goal of this project is to scrape, process, analyze, and visualize cricket match data from Cricsheet. We extract JSON files for various match types (ODI, T20, Test,IPL), store the cleaned data in an SQL database, and build an interactive dashboard using **PowerBI**. The project also involves performing **Exploratory Data Analysis (EDA)** using Python and executing 20 different SQL queries to extract valuable insights.

##  Skills Developed

- **Data Acquisition (Manual)**- Hands-on experience with sourcing and handling data from web repositories, specifically JSON files.
- **Data Processing with Python**- Expertise in transforming raw, nested JSON data using the **Pandas** library.
- **Database Management with SQL**- Practical skills in designing databases, creating tables with appropriate schemas, and writing optimized queries.
- **Data Analysis**- Ability to formulate and execute complex SQL queries to uncover meaningful insights from large datasets.
- **Open Power BI Dashboard**-Created interactive visualizations to showcase key insights.

Technology Stack
- **Data Preprocessing**- Understanding the critical steps of cleaning, structuring, and preparing unstructured data for analysis and storage.

---
## Domain
**Sports Analytics / Data Analysis**



##  Business Use Cases

* **Player Performance Analysis:** Compare player performance across different match formats.
* **Team Insights:** Analyze team statistics and identify win/loss trends.
* **Match Outcomes:** Identify victory margins, winning patterns, and key strategies.
* **Strategic Decision-Making:** Provide data-driven insights to help analysts and coaches.
* **Fan Engagement:** Offer an interactive dashboard for cricket enthusiasts to explore data.

---

##  Tech Stack & Tools

* **Python:** Pandas, Matplotlib, Seaborn, Plotly
* **SQL:** MySQL/SQLite, SQLAlchemy
* **powerBI**
* **Git & GitHub**
* **Jupyter Notebook**
* **Cricsheet:** JSON Data Source

---

##  Project Approach

### 1. Data Scraping

* Manually download JSON files for Test, ODI, T20, and IPL matches from Cricsheet[Cricsheet](https://cricsheet.org/matches/)..
* Store these files locally for further processing.

### 2. Data Transformation

* Parse the JSON files using **Pandas**.
* Create separate DataFrames for each match format (Test, ODI, T20,IPL).

### 3. Database Management

* Set up an SQL database (e.g., SQLite).
* Design and create tables: `test_matches`, `odi_matches`, `t20_matches`.
* Insert the cleaned data into the respective tables using **SQL**.

### 4. SQL Queries for Data Analysis

Write at least 20 SQL queries to extract insights, such as:

* Top 10 batsmen by total runs in ODIs.
* Leading wicket-takers in T20 matches.
* Team with the highest win percentage in Tests.
* Total number of centuries across all match formats.
* Matches with the narrowest victory margin.

### 5. Exploratory Data Analysis (EDA)

* Generate 10 visualizations using **Matplotlib**, **Seaborn**, and **Plotly** to highlight key insights.
* Present findings via graphs and summary statistics.

### 6. Power BI Dashboard
- Connect **Power BI** to the SQL database.
- Create an interactive dashboard featuring:
  - **Player performance trends (batting, bowling).**
  - **Match outcomes by teams.**
  - **Win/loss analysis across different formats.**
  - **Comparative statistics of teams and players.**




---

## ✅ Results & Deliverables

* ✅ **Manually Scraped Data:** JSON files from Cricsheet.
* ✅ **Structured SQL Database:** Organized tables for each match type.
* ✅ **SQL Queries:** Insightful analysis on player and team performance.
* ✅ **EDA Visualizations:** Graphical analysis of key match statistics.
* ✅ **Streamlit Dashboard:** Interactive and data-driven visual storytelling.

## Dataset Details
- **Source**: [Cricsheet Match Data](https://cricsheet.org/downloads/)
- **Format**: JSON files for individual cricket matches.
- **Variables**: Player statistics (runs, wickets), match results, teams, overs, deliveries.
- **Preprocessing Steps**:
  - Load JSON files into Python.
  - Normalize and flatten nested data.
  - Clean and structure data for SQL storage.














