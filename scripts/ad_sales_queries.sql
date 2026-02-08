-- ============================================================
-- Ad Sales Revenue Analytics - SQL Queries
-- Dataset: 2,400 advertising campaigns
-- Sources: Sales CRM, Ad Platform, Finance System
-- ============================================================

-- 1. Quarterly Revenue Summary: Budget vs Actual
SELECT
    quarter,
    COUNT(*) AS campaigns,
    ROUND(SUM(booked_revenue), 2) AS total_booked,
    ROUND(SUM(actual_revenue), 2) AS total_actual,
    ROUND(SUM(budget), 2) AS total_budget,
    ROUND((SUM(actual_revenue) - SUM(budget)) / SUM(budget) * 100, 1) AS variance_pct
FROM ad_sales
GROUP BY quarter
ORDER BY quarter;


-- 2. Revenue and Margin by Industry
SELECT
    industry,
    COUNT(*) AS campaigns,
    ROUND(SUM(actual_revenue), 2) AS total_revenue,
    ROUND(AVG(actual_revenue), 2) AS avg_revenue,
    ROUND(AVG(margin_pct), 1) AS avg_margin_pct,
    ROUND(AVG(cpm), 2) AS avg_cpm
FROM ad_sales
GROUP BY industry
ORDER BY total_revenue DESC;


-- 3. Ad Format Performance: CPM, CTR, Revenue
SELECT
    ad_format,
    COUNT(*) AS campaigns,
    ROUND(AVG(cpm), 2) AS avg_cpm,
    ROUND(AVG(ctr) * 100, 2) AS avg_ctr_pct,
    ROUND(SUM(actual_revenue), 2) AS total_revenue,
    ROUND(AVG(margin_pct), 1) AS avg_margin,
    ROUND(AVG(delivery_rate) * 100, 1) AS avg_delivery_pct
FROM ad_sales
GROUP BY ad_format
ORDER BY avg_cpm DESC;


-- 4. Sales Rep Performance with Budget Variance
SELECT
    sales_rep,
    COUNT(*) AS campaigns,
    ROUND(SUM(actual_revenue), 2) AS total_revenue,
    ROUND(SUM(budget), 2) AS total_budget,
    ROUND((SUM(actual_revenue) - SUM(budget)) / SUM(budget) * 100, 1) AS variance_pct,
    ROUND(AVG(margin_pct), 1) AS avg_margin,
    ROUND(SUM(gross_margin), 2) AS total_margin
FROM ad_sales
GROUP BY sales_rep
ORDER BY total_revenue DESC;


-- 5. Account Tier Revenue Comparison
SELECT
    account_tier,
    COUNT(*) AS campaigns,
    ROUND(SUM(actual_revenue), 2) AS total_revenue,
    ROUND(AVG(actual_revenue), 2) AS avg_revenue,
    ROUND(AVG(margin_pct), 1) AS avg_margin,
    ROUND(AVG(cpm), 2) AS avg_cpm
FROM ad_sales
GROUP BY account_tier
ORDER BY avg_revenue DESC;


-- 6. Payment Status & Collections Risk
SELECT
    payment_status,
    COUNT(*) AS campaigns,
    ROUND(SUM(actual_revenue), 2) AS total_revenue,
    ROUND(AVG(actual_revenue), 2) AS avg_revenue
FROM ad_sales
GROUP BY payment_status
ORDER BY total_revenue DESC;


-- 7. Top 20 Campaigns by Revenue
SELECT
    campaign_id,
    advertiser,
    industry,
    ad_format,
    quarter,
    ROUND(actual_revenue, 2) AS revenue,
    ROUND(gross_margin, 2) AS margin,
    ROUND(margin_pct, 1) AS margin_pct,
    cpm,
    ROUND(ctr * 100, 2) AS ctr_pct
FROM ad_sales
ORDER BY actual_revenue DESC
LIMIT 20;
