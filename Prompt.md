## 1. Extraction Prompt
```
You are an expert Snowflake business consultant. Analyze the following customer transcripts and extract use cases across THREE disciplines:

1. Data Analytics (BI dashboards, KPI reports, trend analysis)
2. Data Engineering (pipelines, data quality, ingestion, transformation, orchestration)
3. Data Science & AI (ML models, predictions, recommendations, NLP, anomaly detection)

Transcripts:
{all_content[:18000]}

For each use case also provide:
- A short ROI reason (e.g. "Reduces manual reconciliation by 80%", "Predicts churn 30 days early saving $200K/yr")
- Estimated business value tier: "Quick Win", "Strategic", or "Transformational"
- Which stakeholder benefits most (e.g. "CFO", "VP Sales", "Data Team", "COO")
- A complexity score 1-5 (1=easy, 5=complex)
- An urgency flag: "Immediate", "Near-term", or "Future"

Return ONLY valid JSON:
{
  "metrics": {"pain_point_count": int, "sentiment_score": float, "roadmap_item_count": int, "urgency_level": "Low/Medium/High", "data_maturity": "Foundational/Developing/Advanced"},
  "analytics_usecases": [
    {"name": "...", "roi": "...", "value_tier": "Quick Win|Strategic|Transformational", "stakeholder": "...", "complexity": int, "urgency": "Immediate|Near-term|Future"}
  ],
  "dataengineering_usecases": [
    {"name": "...", "roi": "...", "value_tier": "Quick Win|Strategic|Transformational", "stakeholder": "...", "complexity": int, "urgency": "Immediate|Near-term|Future"}
  ],
  "datascience_usecases": [
    {"name": "...", "roi": "...", "value_tier": "Quick Win|Strategic|Transformational", "stakeholder": "...", "complexity": int, "urgency": "Immediate|Near-term|Future"}
  ],
  "key_themes": ["theme1", "theme2", "theme3"],
  "top_risk": "one sentence describing the biggest risk if action is not taken"
}

```

### Purpose:
Parses uploaded customer transcripts to extract structured use cases across three disciplines (analytics, engineering, data science). It also derives key metrics (pain points, sentiment, roadmap items, urgency, data maturity), identifies key themes, and highlights a top risk. The output is a JSON object that populates the “Use Case Landscape” and “Analysis Overview” sections of the app.


## 2. Market Trends Prompt

```
For a customer in the {industry} industry, provide 3 current market trends or benchmarks relevant to data analytics and AI adoption.
Suggest how these translate into business use cases for this customer.

```
### Purpose:
Generates industry‑specific market intelligence by asking for three relevant trends and how they apply to the customer. The free‑text response is displayed in the “Market Intelligence” panel, providing context that helps the user understand how the identified use cases align with broader industry movements.


## 3. Schema Matching Prompt
```
You are a Snowflake Solutions Engineer. MAP each identified use case to the real customer database,
then propose a live proof-of-concept demo using ACTUAL columns and data.

IDENTIFIED USE CASES:
{chr(10).join(uc_names_by_type)}

DATABASE SCHEMA:
{schema_str}

ACTUAL SAMPLE DATA:
{samples_str}

For EACH use case:
1. Identify which tables and columns directly support it
2. Write a working Snowflake SQL query using REAL column names
3. Assign data confidence: High/Medium/Low

Return JSON array. Each item:
{
  "usecase": "exact use case name",
  "type": "Analytics|Data Engineering|Data Science",
  "tables": ["fully.qualified.table"],
  "columns_used": ["col1", "col2"],
  "sql": "SELECT ... FROM real_table_name ... LIMIT 20",
  "demo_description": "2-sentence description of what demo shows and what business decision it supports",
  "data_confidence": "High|Medium|Low",
  "confidence_reason": "one sentence explaining the confidence level",
  "what_data_proves": "one sentence on what actual data demonstrates for the customer",
  "estimated_effort_days": int,
  "snowflake_features": ["Cortex ML", "Snowpark", "Dynamic Tables", "Streamlit"]
}

CRITICAL: Only use column names that appear in the schema. Return ONLY valid JSON array.

```
### Purpose:
Maps each extracted use case to the actual database schema and sample data. It generates a working SQL query, a demo description, a data confidence score with reasoning, and a list of relevant Snowflake features. The resulting JSON array populates the “Data Match & Demo Selection” tab, enabling users to pick a use case and run a live, data‑driven demo.

## 4. Sales Pitch Prompt
```
You are a Snowflake Sales Engineer. Write a short, punchy customer pitch for one use case.

Customer: {customer_name} | Industry: {industry} | Stakeholder: {holder}
Use Case: {selected_match['usecase']}
ROI: {roi_val}
What the live data just showed: {proof}
Time to value: {ttv}

Return EXACTLY this structure. Keep each point to 1-2 sentences maximum.

🔴 THE PROBLEM
One sentence: what pain is the customer feeling right now?

💡 WHAT THIS SOLVES
One sentence: what does this use case enable them to do that they can't today?

📊 WHAT THE DATA SHOWS
One sentence: reference the live demo data — what does it specifically reveal?

💰 THE BUSINESS BENEFIT
One sentence: the concrete ROI or measurable outcome they will see.

⏱️ HOW QUICKLY
Time to value and what the first milestone looks like.

✅ WHY SNOWFLAKE
One sentence: the single most compelling reason Snowflake is the right platform for this.

Keep the entire output under 150 words. No section should exceed 2 sentences.
```
### Purpose:
Creates a concise, structured sales pitch for a selected use case. It uses the customer context, ROI information, and live demo insights to produce a customer‑friendly narrative with clearly labeled sections. The output is displayed in the “Customer Pitch” panel and can be used directly in presentations or conversations with the client.






