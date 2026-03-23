
# InsightForge – Project Summary

## One‑Page Executive Overview

**InsightForge** is a **prototype application** that transforms raw customer transcripts into actionable business use cases by combining Snowflake Cortex (LLM) with your actual database schema. It enables sales engineers, solutions architects, and data teams to rapidly demonstrate the value of Snowflake to customers – 
using their own data.


### 🎯 Business Problem

Customer conversations happen in Discovery calls, Steering Committee meetings, and Future Deck presentations. These transcripts contain valuable signals about pain points, opportunities, and desired outcomes. However, manually extracting and matching those insights to a customer’s data warehouse is time‑consuming and error‑prone.

**InsightForge solves this by:**
- Automatically identifying use cases from transcripts.
- Linking each use case to real tables and columns.
- Generating live, interactive demos with actual or representative data.
- Providing a ready‑to‑present business case, including ROI, stakeholder, and time to value.

### 🧠 How It Works

1. **Upload Transcripts** – User uploads documents (Discovery, SCC, etc.) via the Streamlit sidebar. Files are stored in a Snowflake `transcripts` table.
2. **Cortex Analysis** – The app calls Snowflake Cortex with a prompt that:
   - Extracts use cases across Analytics, Data Engineering, and Data Science.
   - Includes ROI, value tier, and stakeholder for each.
   - Summarises market trends relevant to the customer’s industry.
3. **Schema Matching** – Using the customer’s selected tables (from `table_metadata`) and actual sample data, a second Cortex prompt maps each use case to:
   - The specific tables and columns that support it.
   - A working SQL query.
   - A confidence score (High/Medium/Low) with justification.
4. **Live Demo** – The user selects a use case. The app:
   - Runs the generated SQL against Snowflake.
   - If the query returns data, displays charts (Plotly) and a data table.
   - If the query fails or returns empty, falls back to **smart dummy data** generated based on the use case name (e.g., “churn” triggers churn‑related dummy data).
5. **Business Case** – The app shows:
   - ROI statement, value tier, stakeholder, and estimated time to value.
   - A “Generate Talking Points” button that uses Cortex to produce a structured pitch.
   - An exportable HTML report containing all charts, SQL, and business case – ready to share with the customer.

### 🔧 Technical Architecture

| Layer                | Technology                               |
|----------------------|------------------------------------------|
| **Presentation**     | Streamlit (Python) with custom CSS       |
| **Data Processing**  | Snowpark Python – executes SQL and Cortex calls |
| **LLM**              | Snowflake Cortex – `mixtral-8x7b` model  |
| **Database**         | Snowflake – stores transcripts, metadata, sample data |
| **Charts**           | Plotly – interactive visualisations      |
| **Export**           | HTML (self‑contained) with embedded Plotly charts |

---

### 📊 Key Metrics (with Sample Data)

| Metric                  | Value (sample)                              |
|-------------------------|---------------------------------------------|
| Time to analyse 3 transcripts | ~15 seconds (Cortex calls)              |
| Number of use cases extracted | 12 (4 per discipline)                      |
| Accuracy of schema matching | High for use cases with clear column mapping |
| Demo fallback success   | 100% – always shows a chart, even without data |

---

### ✅ Strengths (Prototype)

- **No manual mapping** – the LLM infers which tables and columns support each use case.
- **Works with any schema** – as long as `table_metadata` is populated.
- **Graceful degradation** – if SQL fails, smart dummy data keeps the demo alive.
- **Exportable output** – customers leave with a self‑contained HTML file they can print or share.

---

### 🚧 Limitations (to address for production)

- **Security** – SQL injection vulnerabilities due to string interpolation.
- **Error handling** – Cortex calls are not wrapped in try/except; failures break the flow.
- **Scalability** – Truncates transcripts >18,000 characters; may lose context.
- **Maintainability** – All code in a single file; repeated HTML and logic.

---

### 🗺️ Next Steps (if moving to production)

1. **Refactor** the app into modules (UI, data layer, Cortex client, etc.).
2. **Parameterise all SQL** queries to prevent injection.
3. **Add comprehensive error handling** around all external calls.
4. **Implement caching** for repeated Cortex calls (e.g., for same transcripts and tables).
5. **Enhance the dummy data generator** with more domain‑specific realism.
6. **Add user authentication** to restrict access and track usage.

---

### 📦 Deliverables

- Streamlit app source code (`insightforge.py`).
- SQL setup script (`setup.sql`) to create all required Snowflake objects.
- This summary document.
- README with setup and usage instructions.

---

**InsightForge demonstrates how Snowflake Cortex can turn raw customer conversations into live, data‑driven demos in minutes – bridging the gap between business needs and technical implementation.**
