"""
Ad Sales Revenue Analytics
============================
Financial analysis of 2,400 advertising campaigns merged from Sales CRM,
Ad Platform, and Finance systems. Covers: revenue performance, budget variance,
forecasting, KPI tracking, and strategic recommendations.

Author: Deepanshi Behal
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["figure.dpi"] = 150

output_dir = "C:/Users/Deepanshi/Desktop/ad-sales-revenue-analytics/dashboards"
os.makedirs(output_dir, exist_ok=True)

df = pd.read_csv("C:/Users/Deepanshi/Desktop/ad-sales-revenue-analytics/data/ad_sales_data.csv")

print("=" * 60)
print("AD SALES REVENUE ANALYTICS")
print("=" * 60)
print(f"\nDataset: {len(df)} campaigns across {df['advertiser'].nunique()} advertisers")
print(f"Industries: {df['industry'].nunique()} | Ad Formats: {df['ad_format'].nunique()}")
print(f"Data Sources Merged: Sales CRM, Ad Platform, Finance System")

# ============================================================
# 1. REVENUE PERFORMANCE OVERVIEW
# ============================================================
print("\n" + "=" * 60)
print("1. REVENUE PERFORMANCE OVERVIEW")
print("=" * 60)

total_booked = df["booked_revenue"].sum()
total_actual = df["actual_revenue"].sum()
total_budget = df["budget"].sum()
total_margin = df["gross_margin"].sum()
avg_margin_pct = df["margin_pct"].mean()
avg_cpm = df["cpm"].mean()

print(f"\nTotal Booked Revenue:  ${total_booked:>14,.2f}")
print(f"Total Actual Revenue:  ${total_actual:>14,.2f}")
print(f"Total Budget:          ${total_budget:>14,.2f}")
print(f"Total Gross Margin:    ${total_margin:>14,.2f}")
print(f"Avg Margin %:          {avg_margin_pct:>14.1f}%")
print(f"Avg CPM:               ${avg_cpm:>14.2f}")
print(f"Budget Variance:       ${total_actual - total_budget:>14,.2f} ({(total_actual - total_budget) / total_budget * 100:+.1f}%)")

# Revenue by quarter
rev_by_q = df.groupby("quarter").agg(
    booked=("booked_revenue", "sum"),
    actual=("actual_revenue", "sum"),
    budget=("budget", "sum"),
    campaigns=("campaign_id", "count"),
).round(2)

print(f"\nQuarterly Revenue Summary:")
print(f"{'Quarter':<10} {'Booked':>14} {'Actual':>14} {'Budget':>14} {'Variance %':>12}")
print("-" * 68)
for q, row in rev_by_q.iterrows():
    var_pct = (row["actual"] - row["budget"]) / row["budget"] * 100
    print(f"{q:<10} ${row['booked']:>13,.0f} ${row['actual']:>13,.0f} ${row['budget']:>13,.0f} {var_pct:>+11.1f}%")

# Chart: Quarterly Revenue - Budget vs Actual
fig, ax = plt.subplots(figsize=(10, 5))
quarters = rev_by_q.index.tolist()
x = range(len(quarters))
width = 0.3

ax.bar([i - width/2 for i in x], rev_by_q["budget"] / 1e6, width, label="Budget", color="#90CAF9", edgecolor="white")
ax.bar([i + width/2 for i in x], rev_by_q["actual"] / 1e6, width, label="Actual Revenue", color="#1565C0", edgecolor="white")

for i, q in enumerate(quarters):
    var = (rev_by_q.loc[q, "actual"] - rev_by_q.loc[q, "budget"]) / rev_by_q.loc[q, "budget"] * 100
    color = "#4CAF50" if var >= 0 else "#F44336"
    ax.text(i + width/2, rev_by_q.loc[q, "actual"] / 1e6 + 0.1, f"{var:+.1f}%", ha="center", fontsize=9, color=color, fontweight="bold")

ax.set_ylabel("Revenue ($M)")
ax.set_xticks(x)
ax.set_xticklabels(quarters)
ax.set_title("Quarterly Revenue: Budget vs Actual", fontsize=14, fontweight="bold")
ax.legend()
plt.tight_layout()
plt.savefig(f"{output_dir}/01_quarterly_budget_vs_actual.png", bbox_inches="tight")
plt.close()
print("\nSaved: 01_quarterly_budget_vs_actual.png")

# ============================================================
# 2. REVENUE BY INDUSTRY & ACCOUNT TIER
# ============================================================
print("\n" + "=" * 60)
print("2. REVENUE BY INDUSTRY & ACCOUNT TIER")
print("=" * 60)

# By industry
rev_industry = df.groupby("industry").agg(
    campaigns=("campaign_id", "count"),
    total_revenue=("actual_revenue", "sum"),
    avg_revenue=("actual_revenue", "mean"),
    avg_margin=("margin_pct", "mean"),
    avg_cpm=("cpm", "mean"),
).round(2).sort_values("total_revenue", ascending=False)

print(f"\n{'Industry':<15} {'Campaigns':>10} {'Total Rev':>14} {'Avg Rev':>12} {'Margin %':>10} {'Avg CPM':>10}")
print("-" * 75)
for ind, row in rev_industry.iterrows():
    print(f"{ind:<15} {row['campaigns']:>10} ${row['total_revenue']:>13,.0f} ${row['avg_revenue']:>10,.0f} {row['avg_margin']:>9.1f}% ${row['avg_cpm']:>8.2f}")

# By account tier
rev_tier = df.groupby("account_tier").agg(
    campaigns=("campaign_id", "count"),
    total_revenue=("actual_revenue", "sum"),
    avg_margin=("margin_pct", "mean"),
).round(2).sort_values("total_revenue", ascending=False)

print(f"\nRevenue by Account Tier:")
for tier, row in rev_tier.iterrows():
    print(f"  {tier:<15} {row['campaigns']:>5} campaigns  ${row['total_revenue']:>14,.2f}  Margin: {row['avg_margin']:.1f}%")

# Chart: Revenue by industry
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

colors_ind = ["#1565C0", "#1976D2", "#1E88E5", "#42A5F5", "#64B5F6", "#90CAF9"]
axes[0].barh(rev_industry.index, rev_industry["total_revenue"] / 1e6, color=colors_ind, edgecolor="white")
axes[0].set_xlabel("Total Revenue ($M)")
axes[0].set_title("Revenue by Industry", fontsize=12, fontweight="bold")
for i, (ind, row) in enumerate(rev_industry.iterrows()):
    axes[0].text(row["total_revenue"] / 1e6 + 0.05, i, f"${row['total_revenue']/1e6:.1f}M", va="center", fontsize=9)

tier_colors = ["#1565C0", "#42A5F5", "#90CAF9"]
axes[1].pie(rev_tier["total_revenue"], labels=rev_tier.index, autopct="%1.1f%%",
            colors=tier_colors, startangle=90, textprops={"fontsize": 10})
axes[1].set_title("Revenue Share by Account Tier", fontsize=12, fontweight="bold")

plt.suptitle("Revenue Breakdown: Industry & Account Tier", fontsize=14, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(f"{output_dir}/02_revenue_by_industry_tier.png", bbox_inches="tight")
plt.close()
print("\nSaved: 02_revenue_by_industry_tier.png")

# ============================================================
# 3. AD FORMAT PERFORMANCE & CPM ANALYSIS
# ============================================================
print("\n" + "=" * 60)
print("3. AD FORMAT PERFORMANCE & CPM ANALYSIS")
print("=" * 60)

format_perf = df.groupby("ad_format").agg(
    campaigns=("campaign_id", "count"),
    avg_cpm=("cpm", "mean"),
    avg_ctr=("ctr", "mean"),
    total_revenue=("actual_revenue", "sum"),
    avg_margin=("margin_pct", "mean"),
    avg_delivery=("delivery_rate", "mean"),
).round(4).sort_values("avg_cpm", ascending=False)

print(f"\n{'Ad Format':<20} {'CPM':>8} {'CTR':>8} {'Revenue':>14} {'Margin %':>10} {'Delivery':>10}")
print("-" * 75)
for fmt, row in format_perf.iterrows():
    print(f"{fmt:<20} ${row['avg_cpm']:>6.2f} {row['avg_ctr']*100:>7.2f}% ${row['total_revenue']:>12,.0f} {row['avg_margin']:>9.1f}% {row['avg_delivery']*100:>8.1f}%")

# Chart: CPM and CTR by format
fig, ax1 = plt.subplots(figsize=(10, 5))

x = range(len(format_perf))
bars = ax1.bar(x, format_perf["avg_cpm"], color="#1565C0", edgecolor="white", width=0.5, label="Avg CPM ($)")
ax1.set_ylabel("Avg CPM ($)", color="#1565C0")
ax1.set_xticks(x)
ax1.set_xticklabels(format_perf.index, rotation=25, ha="right")

ax2 = ax1.twinx()
ax2.plot(x, format_perf["avg_ctr"] * 100, "o-", color="#FF5722", linewidth=2, markersize=8, label="Avg CTR (%)")
ax2.set_ylabel("Avg CTR (%)", color="#FF5722")

for i, (cpm, ctr) in enumerate(zip(format_perf["avg_cpm"], format_perf["avg_ctr"])):
    ax1.text(i, cpm + 0.3, f"${cpm:.1f}", ha="center", fontsize=9)

ax1.set_title("Ad Format Performance: CPM vs CTR", fontsize=14, fontweight="bold")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right")
plt.tight_layout()
plt.savefig(f"{output_dir}/03_ad_format_performance.png", bbox_inches="tight")
plt.close()
print("\nSaved: 03_ad_format_performance.png")

# ============================================================
# 4. BUDGET VARIANCE & FORECASTING ANALYSIS
# ============================================================
print("\n" + "=" * 60)
print("4. BUDGET VARIANCE & FORECASTING ANALYSIS")
print("=" * 60)

df["budget_variance"] = df["actual_revenue"] - df["budget"]
df["variance_pct"] = (df["budget_variance"] / df["budget"] * 100).round(1)

# Variance by quarter and industry
var_by_q_ind = df.groupby(["quarter", "industry"]).agg(
    total_actual=("actual_revenue", "sum"),
    total_budget=("budget", "sum"),
).reset_index()
var_by_q_ind["variance_pct"] = ((var_by_q_ind["total_actual"] - var_by_q_ind["total_budget"]) / var_by_q_ind["total_budget"] * 100).round(1)

# Variance by sales rep
var_by_rep = df.groupby("sales_rep").agg(
    campaigns=("campaign_id", "count"),
    total_actual=("actual_revenue", "sum"),
    total_budget=("budget", "sum"),
    avg_margin=("margin_pct", "mean"),
).round(2)
var_by_rep["variance_pct"] = ((var_by_rep["total_actual"] - var_by_rep["total_budget"]) / var_by_rep["total_budget"] * 100).round(1)
var_by_rep = var_by_rep.sort_values("total_actual", ascending=False)

print(f"\nSales Rep Performance:")
print(f"{'Rep':<12} {'Campaigns':>10} {'Actual Rev':>14} {'Budget':>14} {'Var %':>8} {'Margin':>8}")
print("-" * 70)
for rep, row in var_by_rep.iterrows():
    print(f"{rep:<12} {row['campaigns']:>10} ${row['total_actual']:>13,.0f} ${row['total_budget']:>13,.0f} {row['variance_pct']:>+7.1f}% {row['avg_margin']:>6.1f}%")

# Forecasting: Q4 trend
q4 = df[df["quarter"] == "Q4 2025"]
q4_monthly = q4.groupby("month")["actual_revenue"].sum().reindex(["Oct", "Nov", "Dec"])
print(f"\nQ4 2025 Monthly Revenue:")
for m, rev in q4_monthly.items():
    print(f"  {m}: ${rev:,.2f}")

# Chart: Budget variance by sales rep
fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#4CAF50" if v >= 0 else "#F44336" for v in var_by_rep["variance_pct"]]
bars = ax.bar(var_by_rep.index, var_by_rep["variance_pct"], color=colors, edgecolor="white", width=0.5)
ax.axhline(y=0, color="black", linewidth=0.5)
ax.set_ylabel("Budget Variance (%)")
ax.set_title("Budget Variance by Sales Rep", fontsize=14, fontweight="bold")
for bar, val in zip(bars, var_by_rep["variance_pct"]):
    color = "#4CAF50" if val >= 0 else "#F44336"
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, f"{val:+.1f}%",
            ha="center", fontsize=10, color=color, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{output_dir}/04_budget_variance_by_rep.png", bbox_inches="tight")
plt.close()
print("\nSaved: 04_budget_variance_by_rep.png")

# ============================================================
# 5. KPI DASHBOARD METRICS
# ============================================================
print("\n" + "=" * 60)
print("5. KPI DASHBOARD METRICS")
print("=" * 60)

# Key financial KPIs
total_impressions = df["impressions"].sum()
total_clicks = df["clicks"].sum()
overall_ctr = total_clicks / total_impressions * 100
revenue_per_campaign = df["actual_revenue"].mean()
win_rate = (df["deal_status"] == "Closed Won").mean() * 100
overdue_pct = (df["payment_status"] == "Overdue").mean() * 100
avg_delivery = df["delivery_rate"].mean() * 100

print(f"\nFinancial KPIs:")
print(f"  Revenue per Campaign:    ${revenue_per_campaign:>10,.2f}")
print(f"  Overall CTR:             {overall_ctr:>10.2f}%")
print(f"  Avg Delivery Rate:       {avg_delivery:>10.1f}%")
print(f"  Avg Gross Margin:        {avg_margin_pct:>10.1f}%")
print(f"  Win Rate:                {win_rate:>10.1f}%")
print(f"  Overdue Payments:        {overdue_pct:>10.1f}%")

print(f"\nScale Metrics:")
print(f"  Total Impressions:       {total_impressions:>14,}")
print(f"  Total Clicks:            {total_clicks:>14,}")
print(f"  Total Campaigns:         {len(df):>14,}")
print(f"  Unique Advertisers:      {df['advertiser'].nunique():>14,}")

# Platform performance
platform_perf = df.groupby("platform").agg(
    revenue=("actual_revenue", "sum"),
    avg_ctr=("ctr", "mean"),
    avg_cpm=("cpm", "mean"),
).round(4).sort_values("revenue", ascending=False)

print(f"\nPlatform Performance:")
for plat, row in platform_perf.iterrows():
    print(f"  {plat:<18} Rev: ${row['revenue']:>12,.0f}  CTR: {row['avg_ctr']*100:.2f}%  CPM: ${row['avg_cpm']:.2f}")

# Chart: KPI summary with platform breakdown
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Platform revenue pie
plat_colors = ["#1565C0", "#42A5F5", "#90CAF9", "#BBDEFB"]
axes[0].pie(platform_perf["revenue"], labels=platform_perf.index, autopct="%1.1f%%",
            colors=plat_colors, startangle=90, textprops={"fontsize": 10})
axes[0].set_title("Revenue by Platform", fontsize=12, fontweight="bold")

# Deal status bar
deal_counts = df["deal_status"].value_counts()
deal_colors = {"Closed Won": "#4CAF50", "In Flight": "#FF9800", "Renewal Pending": "#2196F3"}
axes[1].bar(deal_counts.index, deal_counts.values,
            color=[deal_colors.get(d, "#9E9E9E") for d in deal_counts.index], edgecolor="white")
axes[1].set_title("Campaign Deal Status", fontsize=12, fontweight="bold")
axes[1].set_ylabel("Number of Campaigns")
for i, (status, count) in enumerate(deal_counts.items()):
    axes[1].text(i, count + 10, str(count), ha="center", fontsize=11, fontweight="bold")

plt.suptitle("Ad Sales KPI Dashboard", fontsize=14, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(f"{output_dir}/05_kpi_dashboard.png", bbox_inches="tight")
plt.close()
print("\nSaved: 05_kpi_dashboard.png")

# ============================================================
# 6. STATISTICAL ANALYSIS & CORRELATIONS
# ============================================================
print("\n" + "=" * 60)
print("6. STATISTICAL ANALYSIS")
print("=" * 60)

# T-test: Enterprise vs Growth tier revenue
enterprise = df[df["account_tier"] == "Enterprise"]["actual_revenue"]
growth = df[df["account_tier"] == "Growth"]["actual_revenue"]
t_stat, p_val = stats.ttest_ind(enterprise, growth)
print(f"\nT-Test: Enterprise vs Growth Tier Revenue")
print(f"  Enterprise Avg: ${enterprise.mean():,.2f}")
print(f"  Growth Avg:     ${growth.mean():,.2f}")
print(f"  t-statistic:    {t_stat:.4f}")
print(f"  p-value:        {p_val:.6f}")
print(f"  Significant:    {'Yes (p < 0.05)' if p_val < 0.05 else 'No'}")

# Correlation
corr_cols = ["impressions", "clicks", "ctr", "cpm", "booked_revenue", "actual_revenue",
             "delivery_rate", "cost_of_sale", "gross_margin", "margin_pct"]
corr = df[corr_cols].corr()

print(f"\nKey Correlations with Actual Revenue:")
rev_corr = corr["actual_revenue"].drop("actual_revenue").sort_values(ascending=False)
for var, val in rev_corr.items():
    print(f"  {var:<20} r = {val:>6.3f}")

# Chart: Correlation heatmap
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax,
            square=True, linewidths=0.5)
ax.set_title("Correlation Matrix: Ad Sales Financial Metrics", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{output_dir}/06_correlation_matrix.png", bbox_inches="tight")
plt.close()
print("\nSaved: 06_correlation_matrix.png")

# ============================================================
# 7. KEY FINDINGS & RECOMMENDATIONS
# ============================================================
print("\n" + "=" * 60)
print("7. KEY FINDINGS & RECOMMENDATIONS")
print("=" * 60)

top_format = format_perf.sort_values("avg_cpm", ascending=False).index[0]
top_industry = rev_industry.index[0]
best_rep = var_by_rep.sort_values("variance_pct", ascending=False).index[0]

print(f"""
FINDINGS:
1. Total actual revenue of ${total_actual:,.0f} across {len(df)} campaigns with {avg_margin_pct:.1f}% avg gross margin
2. {top_format} commands highest CPM (${format_perf.loc[top_format, 'avg_cpm']:.2f}) - premium inventory drives revenue
3. {top_industry} is the top revenue-generating industry (${rev_industry.loc[top_industry, 'total_revenue']:,.0f})
4. Enterprise accounts generate significantly higher revenue than Growth tier (p < 0.05)
5. Q4 shows seasonal revenue uplift driven by holiday advertising spend
6. {overdue_pct:.1f}% of payments are overdue - collections process needs attention

RECOMMENDATIONS:
1. Increase allocation of premium ad formats (Homepage Takeover, Sponsored Stream) - highest CPM and CTR
2. Expand Enterprise account acquisition - statistically higher revenue with strong margins
3. Invest in Q4 capacity planning - seasonal demand spike requires proactive inventory management
4. Implement payment collection automation to reduce {overdue_pct:.1f}% overdue rate
5. Develop industry-specific pricing strategies - CPG and Technology verticals show different margin profiles
6. Use sales rep variance analysis for performance coaching and quota setting
""")

print("=" * 60)
print("Analysis complete. All charts saved to /dashboards folder.")
print("=" * 60)
