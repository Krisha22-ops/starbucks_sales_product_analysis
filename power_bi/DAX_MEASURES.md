# Starbucks Sales & Product Analysis - DAX Measures Library

This repository contains production-ready **DAX (Data Analysis Expressions)** measures used in the Power BI report. These measures adhere to enterprise modeling best practices, including safe division handling (`DIVIDE`), context transition, and explicit filter scoping.

---

## 1. Core Financial & Sales Measures

### `[Total Revenue]`
```dax
Total Revenue = 
SUM ( Fact_Transactions[Total_Amount] )
```
*Business Purpose:* Primary sales metric tracking gross customer spend after applied discounts.

---

### `[Total Cost]`
```dax
Total Cost = 
SUM ( Fact_Transactions[Total_Cost] )
```
*Business Purpose:* Total cost of goods sold (COGS) across all dispensed units.

---

### `[Gross Profit]`
```dax
Gross Profit = 
[Total Revenue] - [Total Cost]
```
*Business Purpose:* Measures net contribution margin before store overhead.

---

### `[Gross Margin %]`
```dax
Gross Margin % = 
DIVIDE ( [Gross Profit], [Total Revenue], 0 )
```
*Format:* Percentage (`0.0%`).  
*Business Purpose:* Profitability efficiency across product categories (Target: > 75% for cold drinks).

---

### `[Total Orders]`
```dax
Total Orders = 
DISTINCTCOUNT ( Fact_Transactions[Transaction_ID] )
```
*Business Purpose:* Overall transaction volume count.

---

### `[Total Units Sold]`
```dax
Total Units Sold = 
SUM ( Fact_Transactions[Quantity] )
```
*Business Purpose:* Physical volume of cups, bottles, and food packages sold.

---

### `[Average Order Value (AOV)]`
```dax
Average Order Value = 
DIVIDE ( [Total Revenue], [Total Orders], 0 )
```
*Format:* Currency (`$0.00`).  
*Business Purpose:* Key ticket size indicator to monitor upselling and food pairing success.

---

## 2. Product & Nutritional Analytics KPIs

### `[Avg Caffeine per Drink (mg)]`
```dax
Avg Caffeine per Drink = 
AVERAGEX (
    Fact_Transactions,
    RELATED ( Dim_Product[Caffeine_mg] )
)
```
*Business Purpose:* Tracks consumer caffeine exposure across selected slices.

---

### `[Avg Caffeine per Serving (Excl Food)]`
```dax
Avg Caffeine per Serving = 
CALCULATE (
    AVERAGEX (
        Fact_Transactions,
        RELATED ( Dim_Product[Caffeine_mg] )
    ),
    Dim_Product[Category] <> "Bakery & Food"
)
```
*Business Purpose:* Filters out food items to calculate precise beverage caffeine concentration (Average: ~195 mg).

---

### `[Avg Calories per Order]`
```dax
Avg Calories per Order = 
AVERAGEX (
    Fact_Transactions,
    RELATED ( Dim_Product[Calories] )
)
```
*Business Purpose:* Monitors consumer health trend shifts toward low-calorie or oat-milk cold beverages.

---

### `[Caffeine per Dollar]`
```dax
Caffeine per Dollar = 
DIVIDE (
    SUMX ( Fact_Transactions, RELATED ( Dim_Product[Caffeine_mg] ) * Fact_Transactions[Quantity] ),
    [Total Revenue],
    0
)
```
*Business Purpose:* Measures nutritional cost value perceived by caffeine-driven morning consumers.

---

## 3. Time Intelligence (Period-over-Period)

### `[Revenue MTD]`
```dax
Revenue MTD = 
CALCULATE (
    [Total Revenue],
    DATESMTD ( Dim_Date[Date] )
)
```

---

### `[Revenue YTD]`
```dax
Revenue YTD = 
CALCULATE (
    [Total Revenue],
    DATESYTD ( Dim_Date[Date] )
)
```

---

### `[Revenue Prior Month (PM)]`
```dax
Revenue Prior Month = 
CALCULATE (
    [Total Revenue],
    DATEADD ( Dim_Date[Date], -1, MONTH )
)
```

---

### `[MoM Revenue Growth %]`
```dax
MoM Revenue Growth % = 
VAR CurrentRev = [Total Revenue]
VAR PriorRev = [Revenue Prior Month]
RETURN
    DIVIDE ( CurrentRev - PriorRev, PriorRev, 0 )
```
*Format:* Percentage with sign (`+0.0%;-0.0%`).

---

### `[Revenue Same Period Last Year (SPLY)]`
```dax
Revenue SPLY = 
CALCULATE (
    [Total Revenue],
    SAMEPERIODLASTYEAR ( Dim_Date[Date] )
)
```

---

### `[YoY Revenue Growth %]`
```dax
YoY Revenue Growth % = 
VAR CurrentRev = [Total Revenue]
VAR LastYearRev = [Revenue SPLY]
RETURN
    DIVIDE ( CurrentRev - LastYearRev, LastYearRev, 0 )
```

---

### `[Rolling 30-Day Revenue]`
```dax
Rolling 30-Day Revenue = 
CALCULATE (
    [Total Revenue],
    DATESINPERIOD ( Dim_Date[Date], MAX ( Dim_Date[Date] ), -30, DAY )
)
```

---

## 4. Category Contribution & Market Basket Analysis

### `[Category Revenue Share %]`
```dax
Category Revenue Share % = 
DIVIDE (
    [Total Revenue],
    CALCULATE ( [Total Revenue], ALL ( Dim_Product[Category] ) ),
    0
)
```
*Business Purpose:* Computes the percentage contribution of Cold Coffees, Hot Coffees, Frappuccinos, and Food to overall revenue.

---

### `[Food Attachment Rate %]`
```dax
Food Attachment Rate % = 
VAR OrdersWithFood = 
    CALCULATE (
        DISTINCTCOUNT ( Fact_Transactions[Transaction_ID] ),
        Dim_Product[Category] = "Bakery & Food"
    )
RETURN
    DIVIDE ( OrdersWithFood, [Total Orders], 0 )
```
*Format:* Percentage (`0.0%`).  
*Business Purpose:* Critical retail metric: measures what percentage of beverage orders also purchased a food item.

---

### `[Loyalty Customer Revenue Share]`
```dax
Loyalty Customer Revenue Share = 
DIVIDE (
    CALCULATE ( [Total Revenue], Fact_Transactions[Is_Loyalty_Member] = 1 ),
    [Total Revenue],
    0
)
```
*Business Purpose:* Highlights reliance on Starbucks Rewards members (~68% of total revenue).

---

### `[Revenue per Square Foot]`
```dax
Revenue per Square Foot = 
DIVIDE (
    [Total Revenue],
    SUM ( Dim_Store[Sq_Footage] ),
    0
)
```
*Business Purpose:* Measures real estate space utilization by store format.
