"""
Generate simulated Ad Sales Revenue dataset (2,400 rows)
for Ad Sales Revenue Analytics project.
Simulates advertising campaign data merged from Sales CRM, Ad Platform, and Finance systems.
"""

import numpy as np
import pandas as pd

np.random.seed(42)
n = 2400

# ---- SOURCE 1: Campaign & Client Info (Sales CRM) ----
campaign_ids = range(5001, 5001 + n)

advertisers = np.random.choice(
    ["Nike", "Samsung", "Coca-Cola", "Toyota", "Netflix", "Spotify", "Adobe",
     "Microsoft", "PepsiCo", "Procter & Gamble", "Unilever", "Meta", "Apple",
     "Disney", "Warner Bros", "Sony", "EA Games", "Riot Games", "Red Bull", "Intel"],
    n
)

industry = {
    "Nike": "Retail", "Samsung": "Technology", "Coca-Cola": "CPG", "Toyota": "Automotive",
    "Netflix": "Entertainment", "Spotify": "Entertainment", "Adobe": "Technology",
    "Microsoft": "Technology", "PepsiCo": "CPG", "Procter & Gamble": "CPG",
    "Unilever": "CPG", "Meta": "Technology", "Apple": "Technology",
    "Disney": "Entertainment", "Warner Bros": "Entertainment", "Sony": "Technology",
    "EA Games": "Gaming", "Riot Games": "Gaming", "Red Bull": "CPG", "Intel": "Technology",
}
industries = [industry[a] for a in advertisers]

account_tier = np.random.choice(["Enterprise", "Mid-Market", "Growth"], n, p=[0.30, 0.45, 0.25])

sales_rep = np.random.choice(
    ["Sarah K.", "James L.", "Maria G.", "David R.", "Priya S.", "Alex T."], n
)

# ---- SOURCE 2: Campaign Performance (Ad Platform) ----
ad_format = np.random.choice(
    ["Video Pre-Roll", "Display Banner", "Homepage Takeover", "Sponsored Stream",
     "Interactive Overlay", "Audio Ad"], n, p=[0.30, 0.20, 0.10, 0.20, 0.10, 0.10]
)

platform = np.random.choice(["Desktop", "Mobile", "CTV", "Multi-Platform"], n, p=[0.25, 0.35, 0.15, 0.25])

quarter = np.random.choice(["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025"], n, p=[0.20, 0.25, 0.25, 0.30])
month_map = {
    "Q1 2025": ["Jan", "Feb", "Mar"],
    "Q2 2025": ["Apr", "May", "Jun"],
    "Q3 2025": ["Jul", "Aug", "Sep"],
    "Q4 2025": ["Oct", "Nov", "Dec"],
}
months = [np.random.choice(month_map[q]) for q in quarter]

impressions = np.random.lognormal(mean=12, sigma=0.8, size=n).astype(int)
impressions = np.clip(impressions, 50000, 10000000)

# CTR influenced by ad format
base_ctr = np.random.normal(0.015, 0.005, n)
ctr_boost = np.where(ad_format == "Video Pre-Roll", 0.008, 0) + \
            np.where(ad_format == "Homepage Takeover", 0.012, 0) + \
            np.where(ad_format == "Sponsored Stream", 0.010, 0) + \
            np.where(ad_format == "Interactive Overlay", 0.006, 0)
ctr = np.clip(base_ctr + ctr_boost, 0.002, 0.06).round(4)
clicks = (impressions * ctr).astype(int)

# CPM influenced by format and tier
base_cpm = np.random.normal(18, 5, n)
cpm_adj = np.where(ad_format == "Homepage Takeover", 15, 0) + \
          np.where(ad_format == "Video Pre-Roll", 8, 0) + \
          np.where(ad_format == "Sponsored Stream", 10, 0) + \
          np.where(account_tier == "Enterprise", 3, 0) + \
          np.where(quarter == "Q4 2025", 5, 0)
cpm = np.clip(base_cpm + cpm_adj, 5, 55).round(2)

# ---- SOURCE 3: Financial Data (Finance System) ----
# Booked revenue = impressions * CPM / 1000
booked_revenue = (impressions * cpm / 1000).round(2)

# Budget (planned revenue - slightly different from actual)
budget_variance_pct = np.random.normal(0, 0.12, n)
budget = (booked_revenue / (1 + budget_variance_pct)).round(2)

# Actual revenue recognized (may differ from booked due to delivery)
delivery_rate = np.clip(np.random.normal(0.92, 0.08, n), 0.60, 1.05).round(3)
actual_revenue = (booked_revenue * delivery_rate).round(2)

# Cost of sale
cost_pct = np.clip(np.random.normal(0.35, 0.10, n), 0.15, 0.65).round(3)
cost_of_sale = (actual_revenue * cost_pct).round(2)

# Gross margin
gross_margin = (actual_revenue - cost_of_sale).round(2)
margin_pct = np.where(actual_revenue > 0, (gross_margin / actual_revenue * 100).round(1), 0)

# Deal status
deal_status = np.random.choice(["Closed Won", "Closed Won", "Closed Won", "In Flight", "Renewal Pending"], n, p=[0.50, 0.05, 0.05, 0.25, 0.15])

# Payment status
payment_status = np.where(
    deal_status == "In Flight", "Pending",
    np.random.choice(["Received", "Invoiced", "Overdue"], n, p=[0.55, 0.30, 0.15])
)

# ---- BUILD DATAFRAME ----
df = pd.DataFrame({
    "campaign_id": campaign_ids,
    "advertiser": advertisers,
    "industry": industries,
    "account_tier": account_tier,
    "sales_rep": sales_rep,
    "ad_format": ad_format,
    "platform": platform,
    "quarter": quarter,
    "month": months,
    "impressions": impressions,
    "clicks": clicks,
    "ctr": ctr,
    "cpm": cpm,
    "booked_revenue": booked_revenue,
    "budget": budget,
    "actual_revenue": actual_revenue,
    "delivery_rate": delivery_rate,
    "cost_of_sale": cost_of_sale,
    "gross_margin": gross_margin,
    "margin_pct": margin_pct,
    "deal_status": deal_status,
    "payment_status": payment_status,
})

# Save
df.to_csv("C:/Users/Deepanshi/Desktop/ad-sales-revenue-analytics/data/ad_sales_data.csv", index=False)
print(f"Dataset created: {len(df)} campaigns")
print(f"\nIndustries:\n{df['industry'].value_counts()}")
print(f"\nAd Formats:\n{df['ad_format'].value_counts()}")
print(f"\nTotal Booked Revenue: ${df['booked_revenue'].sum():,.2f}")
print(f"Total Actual Revenue: ${df['actual_revenue'].sum():,.2f}")
print(f"Total Budget: ${df['budget'].sum():,.2f}")
print(f"Avg Margin %: {df['margin_pct'].mean():.1f}%")
print(f"Avg CPM: ${df['cpm'].mean():.2f}")
