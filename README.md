# Ad Sales Revenue Analytics

End-to-end financial analysis of 2,400 advertising campaigns merged from three data sources (Sales CRM, Ad Platform, Finance System). Covers revenue performance, budget variance analysis, KPI tracking, ad format profitability, forecasting, and strategic recommendations.

## Project Structure

```
ad-sales-revenue-analytics/
├── data/
│   └── ad_sales_data.csv                # 2,400-row merged dataset
├── scripts/
│   ├── generate_data.py                 # Simulates multi-source ad sales data
│   └── ad_sales_queries.sql             # 7 SQL queries for financial analysis
├── notebooks/
│   └── ad_sales_analysis.py             # Full financial analysis with KPI tracking
├── dashboards/
│   ├── 01_quarterly_budget_vs_actual.png
│   ├── 02_revenue_by_industry_tier.png
│   ├── 03_ad_format_performance.png
│   ├── 04_budget_variance_by_rep.png
│   ├── 05_kpi_dashboard.png
│   └── 06_correlation_matrix.png
└── README.md
```

## Data Sources Simulated

| Source | Fields | Description |
|--------|--------|-------------|
| Sales CRM | advertiser, industry, account_tier, sales_rep | Client and deal info |
| Ad Platform | ad_format, platform, impressions, clicks, CTR, CPM | Campaign performance |
| Finance System | booked_revenue, budget, actual_revenue, cost_of_sale, gross_margin, payment_status | Financial data |

## Analysis Sections

1. **Revenue Performance Overview** - Quarterly budget vs actual with variance analysis
2. **Revenue by Industry & Account Tier** - Industry profitability and tier segmentation
3. **Ad Format Performance** - CPM vs CTR analysis across video, display, sponsored formats
4. **Budget Variance & Forecasting** - Sales rep performance, Q4 trend analysis
5. **KPI Dashboard** - Financial KPIs, platform breakdown, deal pipeline status
6. **Statistical Analysis** - T-tests, correlation matrix across all financial metrics

## Key Findings

- **$13.4M** total actual revenue across 2,400 campaigns with **64.9%** avg gross margin
- Homepage Takeover commands highest CPM ($36.02) - premium inventory drives revenue
- Technology is the top revenue-generating vertical ($4.7M)
- Q4 shows seasonal revenue uplift driven by holiday advertising spend
- 11.5% of payments are overdue - collections process improvement opportunity
- Budget variance of -9.2% indicates forecasting model needs refinement

## Financial KPIs Tracked

| KPI | Value |
|-----|-------|
| Revenue per Campaign | $5,581 |
| Overall CTR | 2.13% |
| Avg Delivery Rate | 91.8% |
| Avg Gross Margin | 64.9% |
| Win Rate | 60.4% |
| Overdue Rate | 11.5% |

## Tools Used

- **Python**: pandas, numpy, matplotlib, seaborn, scipy.stats
- **SQL**: Revenue aggregation, variance analysis, rep performance, collections risk
- **Statistical Methods**: T-tests, Pearson correlation, budget variance analysis
- **Financial Concepts**: Budget vs Actual, CPM/CTR analysis, margin analysis, KPI frameworks

## How to Run

```bash
pip install pandas numpy matplotlib seaborn scipy
python scripts/generate_data.py
python notebooks/ad_sales_analysis.py
```

## Author

Deepanshi Behal | [LinkedIn](https://linkedin.com/in/bdeepanshi) | [GitHub](https://github.com/behaldeepanshi01-gif)
