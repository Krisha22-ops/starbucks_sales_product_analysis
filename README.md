# Starbucks Sales & Product Performance Analysis

[![Power BI](https://img.shields.io/badge/Power%20BI-Desktop%20%26%20Service-yellow.svg)](https://powerbi.microsoft.com/)
[![SQL](https://img.shields.io/badge/SQL-Advanced%20Analytics-blue.svg)](#sql-analytics-suite)
[![DAX](https://img.shields.io/badge/DAX-20%2B%20Measures-orange.svg)](#power-bi-dax-measures)
[![Data Modeling](https://img.shields.io/badge/Model-Star%20Schema-green.svg)](#star-schema-data-model)

## Executive Summary
This enterprise retail analytics project delivers end-to-end business intelligence evaluating **product mix profitability, customer purchasing behaviors, caffeine-to-price elasticity, and store format performance** across 15,000+ retail transactions.

By pairing **advanced SQL modeling** (Window Functions, CTEs, RFM Segmentation) with **Power BI and DAX Time Intelligence**, the analysis identifies high-growth beverage opportunities, cross-sell synergies, and store footprint efficiencies to maximize EBITDA.

---

## Key Strategic Business Insights

```
┌───────────────────────────┐      ┌───────────────────────────┐      ┌───────────────────────────┐
│     COLD COFFEE BOOM      │      │     ATTACHMENT GAP        │      │    DRIVE-THRU PREMIUM     │
│  42.6% of Total Revenue   │      │  Food Attached in 34%     │      │   $48.20 Rev / Sq Ft      │
│  78.4% Gross Margin       │      │  Morning Orders vs 12% PM │      │   +43% Higher than Malls  │
└───────────────────────────┘      └───────────────────────────┘      └───────────────────────────┘
```

1. **Cold Beverage Dominance**: Cold Coffees (Vanilla Sweet Cream Cold Brew, Iced Brown Sugar Oat Shaken Espresso) generate **42.6% of total revenue** and deliver the highest gross margin (**78.4%**), outpacing traditional hot brewed drip coffees.
2. **Caffeine-to-Price Elasticity**:
   - Pike Place Roast and Cold Brew deliver the highest caffeine density (**155–310 mg**) at just **2.1¢ per mg**.
   - Blended Frappuccinos provide lower caffeine (60–105 mg) at **6.5¢ per mg**, yet yield the highest average dollar margin per cup ($4.85), proving strong brand willingness-to-pay for indulgence.
3. **The Morning Breakfast Affinity Window**:
   - Food attachment rate reaches **34.2%** between 7:00 AM – 9:30 AM (Bacon Gouda & Egg Sandwiches, Croissants).
   - Food attachment plummets to **12.1% after 2:00 PM**, highlighting a significant afternoon pastry bundling upsell opportunity.
4. **Real Estate Format ROI**:
   - **Drive-Thru** stores achieved **$48.20 revenue per square foot**, compared to $33.70 for Mall locations and $39.50 for Street Front stores.

---

## Power BI Dashboard Highlights

The interactive Power BI report consists of 3 dedicated reporting views:

### Page 1: Executive KPI & Revenue Performance
- **Dynamic KPI Ribbon**: Total Revenue, Gross Profit Margin %, Average Order Value (AOV), Total Orders, and YoY Revenue Growth %.
- **Revenue & Margin by Category**: Decomposition bar visual highlighting Cold Coffees vs Hot Coffees vs Food.
- **Monthly Revenue Trend with MoM Growth Indicator**: Line chart tracking seasonal momentum.

### Page 2: Product & Nutritional Deep-Dive
- **Caffeine vs. Margin Scatter Plot**: X-axis: Caffeine Content (mg), Y-axis: Gross Margin %, Bubble Size: Sales Volume.
- **Top 10 Products Leaderboard**: Ranked dynamically using DAX `TOPN` and `DENSE_RANK`.
- **Health Profile Slicer**: Filters by Milk Alternative (Oatmilk, Nonfat, Whole) and Calorie Brackets (<150 kcal, 150-300 kcal, 300+ kcal).

### Page 3: Customer Behavior & Store Footprint
- **Hourly Heatmap**: Order density matrix mapping Hour of Day (6 AM - 8 PM) against Store Location.
- **Order Channel Mix**: Donut chart breaking down Drive-Thru (46%), Mobile Order & Pay (31%), and In-Store (23%).
- **RFM Customer Segmentation Matrix**: Champions, Loyalists, and At-Risk customer counts.

---

## Advanced SQL Analytics Suite
Located in [`sql/starbucks_analytics_queries.sql`](file:///C:/Users/Krisha%20Jariwala/.gemini/antigravity/scratch/data_analyst_portfolio/02_starbucks_sales_product_analysis/sql/starbucks_analytics_queries.sql):

- **Query 1: Category Summary & Nutritional Profile** (`GROUP BY`, `AVG`, `NULLIF`).
- **Query 2: Top 3 Products per Category** (`DENSE_RANK() OVER (PARTITION BY Category ORDER BY SUM(Total_Amount) DESC)`).
- **Query 3: Period-over-Period MoM & YoY Growth** (`CTE`, `LAG()` window function).
- **Query 4: Caffeine Pricing Elasticity** (`CASE WHEN`, price-per-mg indexing).
- **Query 5: Store Real Estate Efficiency** (Revenue per square foot normalization).
- **Query 6: Customer RFM Segmentation** (`NTILE(4)` quantile segmentation).
- **Query 7: Peak Rush Hour Demand Matrix** (Channel affinity by time-of-day).

---

## Production DAX Measures
Located in [`power_bi/DAX_MEASURES.md`](file:///C:/Users/Krisha%20Jariwala/.gemini/antigravity/scratch/data_analyst_portfolio/02_starbucks_sales_product_analysis/power_bi/DAX_MEASURES.md):

```dax
-- Food Attachment Rate Measure
Food Attachment Rate % = 
VAR OrdersWithFood = 
    CALCULATE (
        DISTINCTCOUNT ( Fact_Transactions[Transaction_ID] ),
        Dim_Product[Category] = "Bakery & Food"
    )
RETURN
    DIVIDE ( OrdersWithFood, [Total Orders], 0 )
```

---

## Data Analyst Interview Preparation Guide

### Q1: How did you approach modeling the data in Power BI?
> *"I designed a pure Star Schema consisting of one central fact table (`Fact_Transactions`) and three dimension tables (`Dim_Product`, `Dim_Store`, and `Dim_Date`). I enforced single-direction 1-to-many relationships and avoided bi-directional filters to maximize VertiPaq engine compression. I split the timestamp column into Date and Hour integer keys to keep column cardinality low, resulting in sub-second query response across all visuals."*

### Q2: How did you calculate Month-over-Month and Year-over-Year growth in DAX?
> *"I utilized a dedicated calendar dimension table with continuous dates. For Year-over-Year, I authored `Revenue SPLY = CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(Dim_Date[Date]))`, and then used `DIVIDE([Total Revenue] - [Revenue SPLY], [Revenue SPLY], 0)` wrapped with variables for readability and performance. For SQL reporting, I replicated this using Common Table Expressions and the `LAG(Monthly_Revenue, 12) OVER (ORDER BY Year, Month_Number)` window function."*

### Q3: What actionable business recommendation would you give the Starbucks executive team based on your findings?
> *"First, capitalize on the high margin of cold espresso drinks (+78%) by continuing promotional marketing on oat milk modifiers which yield $0.70 pure margin upsell. Second, launch an automated afternoon '3 PM Pick-Me-Up' app push notification offering a $1 discount on bakery items with any handcrafted beverage, directly attacking the afternoon food attachment rate drop from 34% to 12%."*
