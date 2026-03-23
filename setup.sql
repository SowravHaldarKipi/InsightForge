-- =============================================================================
-- InsightForge – Setup Script (Minimal)
-- Creates the necessary Snowflake objects for the InsightForge demo app.
-- =============================================================================

-- Use ACCOUNTADMIN to have sufficient privileges
USE ROLE ACCOUNTADMIN;

-- Create the database and schema (if they don't exist)
CREATE DATABASE IF NOT EXISTS COCO_HACKATHON_DB;
CREATE SCHEMA IF NOT EXISTS COCO_HACKATHON_DB.CORE_DATA;

-- Set the context
USE DATABASE COCO_HACKATHON_DB;
USE SCHEMA CORE_DATA;
USE WAREHOUSE COMPUTE_WH;   -- or any warehouse you have

-- =============================================================================
-- 1. Transcripts table – stores uploaded documents
-- =============================================================================
CREATE OR REPLACE TABLE transcripts (
    doc_id      INT AUTOINCREMENT,
    filename    STRING,
    doc_type    STRING,               -- 'Discovery', 'SCC', 'Future Deck', 'ARB', 'Other'
    content     STRING,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Insert a few sample transcripts to demonstrate functionality
INSERT INTO transcripts (filename, doc_type, content) VALUES
('discovery_acme.txt', 'Discovery', 
 'Customer: Acme Corp is facing delays in financial reporting. Their current ETL takes 3 days. They want real-time dashboards. They are considering Snowflake but worried about cost. They also mentioned data silos between sales and finance.'),
('scc_q2_2024.txt', 'SCC', 
 'Sales team reports that Acme Corp is unhappy with payment processing times. Sentiment: frustrated. They want to see customer payment trends. Potential upsell: AI-based payment prediction.'),
('future_deck_acme.txt', 'Future Deck', 
 'We presented the new customer 360 dashboard. Acme was impressed. They asked about churn prediction and cross-sell opportunities. They plan to expand to EU next year, need multi-currency support.');

-- =============================================================================
-- 2. Sample business data table (sales_data) – used for live demos
-- =============================================================================
CREATE OR REPLACE TABLE sales_data AS
SELECT * FROM VALUES
  (1, 'Acme Corp', 'Gold', 'Enterprise License', 'Software', 50000.00, '2024-09-15', 'Net 30'),
  (2, 'Acme Corp', 'Gold', 'Premium Support', 'Services', 5000.00, '2024-08-20', 'Net 15'),
  (3, 'Beta LLC', 'Silver', 'Standard License', 'Software', 10000.00, '2024-09-10', 'Net 30'),
  (4, 'Beta LLC', 'Silver', 'Consulting', 'Services', 3500.00, '2024-09-11', 'Net 15'),
  (5, 'Gamma Inc', 'Bronze', 'Basic License', 'Software', 2000.00, '2024-10-01', 'Net 45'),
  (6, 'Acme Corp', 'Gold', 'Enterprise License Renewal', 'Software', 55000.00, '2024-10-05', 'Net 30')
  AS t(sale_id, customer_name, customer_tier, product_name, category, sale_amount, sale_date, payment_terms);

-- =============================================================================
-- 3. Table metadata – automatically reflects all tables in the schema
-- =============================================================================
CREATE OR REPLACE TABLE table_metadata AS
SELECT 
    table_catalog || '.' || table_schema || '.' || table_name AS fully_qualified_table_name,
    column_name,
    data_type
FROM COCO_HACKATHON_DB.INFORMATION_SCHEMA.COLUMNS 
WHERE table_schema = 'CORE_DATA';

-- (Optional) Refresh metadata when new tables are added:
-- INSERT INTO table_metadata ... (run manually or schedule a task)

-- =============================================================================
-- 4. Cortex function – wraps the Cortex COMPLETE endpoint
-- =============================================================================
CREATE OR REPLACE FUNCTION cortex_complete(prompt_text STRING)
RETURNS STRING
AS
$$
    SNOWFLAKE.CORTEX.COMPLETE(
        'mixtral-8x7b',   -- model available in many regions
        prompt_text
    )
$$;

-- Test the function (optional)
-- SELECT cortex_complete('What is 2+2?') AS answer;

-- =============================================================================
-- 5. (Optional) Additional tables if needed for extended demos
-- =============================================================================
-- If you want more tables to show in the table selector, create them here.
-- For example, a marketing_spend table (used by the dummy data generator)
CREATE OR REPLACE TABLE marketing_spend AS
SELECT * FROM VALUES
  (1, 'Google Ads', 12000.00, 150000, 4500, '2024-09-01', 'NA'),
  (2, 'Google Ads', 5000.00, 60000, 1200, '2024-09-15', 'EU'),
  (3, 'LinkedIn', 8000.00, 40000, 800, '2024-09-05', 'NA')
  AS t(campaign_id, channel, spend_amount, impressions, clicks, campaign_date, region);

-- =============================================================================
-- Verify setup
-- =============================================================================
SELECT 'Setup complete' AS status;




