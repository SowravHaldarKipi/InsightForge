# InsightForge – Snowflake Cortex AI Business Use Case Generator

[![Streamlit App](https://img.shields.io/badge/Streamlit-App-brightgreen)](https://streamlit.io)
[![Snowflake](https://img.shields.io/badge/Snowflake-Cortex-blue)](https://www.snowflake.com/cortex/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**InsightForge** is a prototype application that uses Snowflake Cortex and Streamlit to automatically extract business use cases from uploaded customer transcripts, map them to your actual database schema, and generate live interactive demos – all with zero manual configuration.

---

## ✨ Features

- 📄 **Upload transcripts** – Discovery calls, Steering Committee (SCC) decks, Future Deck presentations, etc.
- 🧠 **Cortex-powered analysis** – Extracts use cases across Analytics, Data Engineering, and Data Science, complete with ROI statements, value tiers, and stakeholders.
- 📊 **Market intelligence** – Fetches relevant industry trends and benchmarks.
- 🔗 **Schema matching** – Maps each use case to actual tables and columns in your Snowflake database.
- ✅ **Confidence scoring** – Shows how well your existing data supports each use case (High/Medium/Low).
- 🎛️ **Live demo generation** – Select a use case, run a real SQL query against your data (or fall back to smart dummy data), and display interactive charts with Plotly.
- 📈 **ROI & business case** – Displays value tier, stakeholder, time to value, and a Cortex-generated sales pitch.
- 📄 **Exportable demo pack** – HTML report with charts, SQL, and business case, ready to present to customers.

---

## 🏗️ Architecture Overview

<img width="1766" height="1148" alt="_- visual selection (33)" src="https://github.com/user-attachments/assets/aa5f5876-2742-4baa-ae24-3c42262808d2" />


- **Streamlit** – provides the interactive dashboard and file upload.
- **Snowpark** – executes SQL and calls the Cortex functions.
- **Cortex** – completes prompts for use case extraction, market research, and schema matching.
- **Plotly** – renders interactive charts from the demo data.

---

## 🧰 Prerequisites

- A **Snowflake account** with the `ACCOUNTADMIN` role (or equivalent privileges) to create the required database objects.
- The **Snowflake Notebook** environment or a local Python environment with `snowflake-snowpark-python` and `streamlit` installed.
- A **warehouse** (e.g., `COMPUTE_WH`) for running queries.
- Snowflake **Cortex** must be enabled (available in many regions).

---

## 🚀 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-org/insightforge.git
cd insightforge
```

### 2. Set up the Snowflake database
```
Run the provided SQL script (setup.sql) in your Snowflake environment (Snowsight or a SQL client). This creates:

COCO_HACKATHON_DB database and CORE_DATA schema.

All required tables: transcripts, table_metadata, projects, incidents, sales_data, etc.

The cortex_complete function (using the mixtral-8x7b model).

```

### 3. Configure the app
The app expects a Snowflake session to be active. If you are running it inside a Snowflake Notebook, the session is automatically provided via get_active_session().
For local development, you would need to modify the code to create a session using connection parameters (not covered here).

### 4. Run the Streamlit app
Inside the Snowflake Notebook, you can simply paste the code into a cell and run it. For local testing (with a modified session), use:

```
streamlit run insightforge.py
```

### 📖 How to Use

```
1.Upload transcripts – In the sidebar, choose the document type (Discovery, SCC, etc.) and upload .txt, .md, or .csv files.

2.Select tables – Choose the tables you want to analyse. The app automatically fetches their columns from table_metadata.

3.Click “Analyze & Generate Use Cases” – The app will:
- Run Cortex on the transcripts to extract use cases.
- Fetch market trends for your industry.
- Map each use case to your selected tables using the actual schema and sample data.

4.Review results – Use the tabs to browse use cases by category. Tick “Add to Demo” for any you want to focus on.

5.Select a use case for demo – Pick one from the dropdown in the “Data Match & Demo Selection” section. The app shows:
- Confidence level, tables/columns used, and the generated SQL.
- An ROI card with value tier, stakeholder, and time to value.
- A live demo dashboard (with real data if the SQL works, otherwise smart dummy data).

6.Generate a sales pitch – Click “Generate Talking Points with Cortex” to get a structured pitch.

7.Export – Download the full demo pack as an HTML file (open in browser, then print as PDF).
```

## 🧪 Demo Walkthrough (with sample data)
```
The setup script loads sample data including:

- A few transcripts (Discovery, SCC, Future Deck) for a fictitious customer “Acme Corp”.

- A sales_data table with real‑world sales records.

- A table_metadata view that lists all tables and columns.

- When you run the analysis with these, you’ll see:
A list of use cases like “Customer Payment Delay Dashboard” and “Customer Churn Prediction Model”.
High/Medium/Low confidence matches to the sales_data table.
A live demo dashboard for “Customer Payment Delay Dashboard” that shows actual data from the sales_data table (because the generated SQL works).
This demonstrates the full pipeline from transcript → use case → data match → live demo.
```

## 🛠️ Technology Stack
<img width="1756" height="1440" alt="_- visual selection (34)" src="https://github.com/user-attachments/assets/cd9c3d35-0177-4203-a633-d5d58be3d882" />


## 📁 Project Structure
```
text
insightforge/
├── insightforge.py          # Main Streamlit app
├── setup.sql                # Snowflake database creation script
├── README.md                # This file
├── Project_Summary.md       # One‑page executive summary
├── assets/                  # Screenshots, diagrams (optional)
└── LICENSE                  # MIT License

```
