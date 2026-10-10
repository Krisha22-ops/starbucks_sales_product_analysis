# Starbucks Sales & Product Analytics - Power BI Dashboard Implementation Guide

This guide explains how to view, edit, and publish the **Starbucks Sales & Product Analytics Power BI Dashboard**.

---

## 3 Ways to Access & Present the Dashboard

### Option 1: Live Interactive Browser Dashboard (Zero Setup)
Open the standalone interactive Power BI replica in your web browser:
[`starbucks_power_bi_dashboard.html`](file:///C:/Users/Krisha%20Jariwala/.gemini/antigravity/scratch/data_analyst_portfolio/02_starbucks_sales_product_analysis/power_bi/starbucks_power_bi_dashboard.html)
- Fully interactive slicers (Category, Store Type, Loyalty Member).
- Real-time DAX KPI calculation updates.
- 3 report pages: Executive KPI, Caffeine Elasticity Matrix, and Store Real Estate.
- Ideal for portfolio websites, GitHub Pages, or sharing with recruiters who don't have Power BI Desktop installed!

### Option 2: Native Power BI Desktop Project (`.pbip`)
If you have **Power BI Desktop** installed:
1. Double-click [`Starbucks_Sales_Dashboard.pbip`](file:///C:/Users/Krisha%20Jariwala/.gemini/antigravity/scratch/data_analyst_portfolio/02_starbucks_sales_product_analysis/power_bi/Starbucks_Sales_Dashboard.pbip).
2. Power BI Desktop opens automatically with:
   - Full Star Schema relational model (`Fact_Transactions`, `Dim_Product`, `Dim_Store`, `Dim_Date`).
   - Pre-loaded DAX measures ([`DAX_MEASURES.md`](file:///C:/Users/Krisha%20Jariwala/.gemini/antigravity/scratch/data_analyst_portfolio/02_starbucks_sales_product_analysis/power_bi/DAX_MEASURES.md)).
   - Data source connections pointing directly to your local CSVs.

### Option 3: Build from Scratch in Power BI Desktop (Standard PBIX)
Follow the step-by-step layout specifications below.

---

## Visual Layout & Canvas Specifications (16:9 - 1280 x 720 px)

### Theme & Color Palette
- **Primary Accent:** `#00754A` (Starbucks Deep Green)
- **Secondary Dark:** `#1E3932` (House Dark Forest)
- **Soft Light Accent:** `#D4E9E2` (Warm Foam Green)
- **Data Callout Colors:** `#3B82F6` (Cold Brews), `#F59E0B` (Hot Coffees), `#8B5CF6` (Frappuccino), `#10B981` (Bakery)

---

### Page 1: Executive KPI & Revenue Performance

#### 1. KPI Card Ribbon (Top, Y: 10px, Height: 90px)
Create 6 single-card visuals or a New Card Visual (`Card (new)`):
| Card Title | Measure Expression | Formatting | Callout Value Display |
| :--- | :--- | :--- | :--- |
| **Total Revenue** | `[Total Revenue]` | Currency (`$#,##0.00`) | $92,450 (Green font) |
| **Gross Profit** | `[Gross Profit]` | Currency (`$#,##0.00`) | $69,150 |
| **Gross Margin %**| `[Gross Margin %]` | Percentage (`0.0%`) | 74.8% |
| **Total Orders** | `[Total Orders]` | Integer (`#,##0`) | 15,000 |
| **Avg Order Value**| `[Average Order Value]` | Currency (`$#,##0.00`) | $6.16 |
| **Avg Caffeine** | `[Avg Caffeine per Drink]` | String / Number | 185 mg |

#### 2. Category Revenue Share (Clustered Bar Chart)
- **X-Axis:** `[Total Revenue]`
- **Y-Axis:** `Dim_Product[Category]`
- **Tooltip:** `[Gross Margin %]`, `[Total Units Sold]`
- **Data Labels:** Turn On, Position: Outside End.
- **Color:** Assign `#3B82F6` to Cold Coffees to visually emphasize market dominance (42.6% share).

#### 3. Fulfillment Channel Breakdown (Donut Chart)
- **Legend:** `Fact_Transactions[Order_Channel]`
- **Values:** `[Total Orders]`
- **Details:** Drive-Thru (46%), Mobile Order & Pay (31%), In-Store (23%).

#### 4. Quarterly Revenue Momentum (Line & Clustered Column Chart)
- **Shared X-Axis:** `Dim_Date[Year]`, `Dim_Date[Quarter]`
- **Column Values:** `[Total Revenue]`
- **Line Values:** `[YoY Revenue Growth %]`

---

### Page 2: Product & Caffeine Elasticity Matrix

#### 1. Caffeine vs. Margin Scatter Plot
- **X-Axis:** `Dim_Product[Caffeine_mg]` (Continuous numeric)
- **Y-Axis:** `Dim_Product[Gross_Margin_Pct]` (Continuous percentage)
- **Size:** `[Total Units Sold]`
- **Legend:** `Dim_Product[Category]`
- **Reference Lines:**
  - Constant X-Line at **150 mg** (Moderate caffeine threshold).
  - Constant Y-Line at **75%** (Target margin threshold).
- **Insight:** Highlights Cold Brew in the upper-right high-margin / high-caffeine quadrant.

#### 2. Top 10 Best-Sellers Leaderboard (Table Visual)
- **Columns:** `Dim_Product[Product_Name]`, `Dim_Product[Category]`, `Dim_Product[Size]`, `[Total Revenue]`, `[Gross Margin %]`, `[Avg Caffeine per Drink]`
- **Conditional Formatting:** Add Data Bars to `[Total Revenue]` and Color Scales to `[Gross Margin %]`.

---

### Page 3: Store Format & Hourly Heatmap

#### 1. Store Space Efficiency (Bar Chart)
- **Y-Axis:** `Dim_Store[Store_Type]` (Drive-Thru, Street Front, Airport, Mall)
- **X-Axis:** `[Revenue per Square Foot]`
- **Sort:** Descending (Drive-Thru tops at $48.20/sq ft).

#### 2. Hourly Sales Matrix (Matrix Visual / Heatmap)
- **Rows:** `Fact_Transactions[Hour]` (6 to 20)
- **Columns:** `Dim_Store[Store_Type]`
- **Values:** `[Total Orders]`
- **Conditional Formatting:** Background color gradient (Soft Cream to Dark Forest Green `#00754A`) to reveal peak morning rush between 7:00 AM and 9:30 AM.
