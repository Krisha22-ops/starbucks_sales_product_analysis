-- =====================================================================================
-- STARBUCKS SALES & PRODUCT PERFORMANCE ANALYTICS
-- Database Dialect: ANSI SQL / PostgreSQL / MySQL 8.0+ / Snowflake / MS SQL Server
-- Author: Data Analyst Portfolio
-- Objectives: Pricing trends, category performance, caffeine metrics, RFM segmentation,
--             basket attachment, and store format efficiency.
-- =====================================================================================

-- -------------------------------------------------------------------------------------
-- 1. CATEGORY PERFORMANCE & NUTRITIONAL PROFILE SUMMARY
-- Computes total revenue, units sold, gross profit margin %, and average caffeine (mg).
-- -------------------------------------------------------------------------------------
SELECT 
    p.Category,
    COUNT(DISTINCT t.Transaction_ID) AS Total_Transactions,
    SUM(t.Quantity) AS Total_Units_Sold,
    ROUND(SUM(t.Total_Amount), 2) AS Total_Revenue,
    ROUND(SUM(t.Gross_Profit), 2) AS Total_Gross_Profit,
    ROUND((SUM(t.Gross_Profit) / NULLIF(SUM(t.Total_Amount), 0)) * 100, 2) AS Gross_Margin_Pct,
    ROUND(AVG(p.Caffeine_mg), 1) AS Avg_Caffeine_mg,
    ROUND(AVG(p.Calories), 1) AS Avg_Calories,
    ROUND(AVG(t.Unit_Price), 2) AS Avg_Selling_Price
FROM starbucks_transactions t
JOIN starbucks_products p ON t.Product_ID = p.Product_ID
GROUP BY p.Category
ORDER BY Total_Revenue DESC;


-- -------------------------------------------------------------------------------------
-- 2. TOP 3 PERFORMING PRODUCTS PER CATEGORY (WINDOW FUNCTION: DENSE_RANK)
-- Identifies category leaders to guide inventory allocation and seasonal promotions.
-- -------------------------------------------------------------------------------------
WITH ProductPerformance AS (
    SELECT 
        p.Category,
        p.Product_Name,
        p.Size,
        SUM(t.Quantity) AS Total_Units_Sold,
        ROUND(SUM(t.Total_Amount), 2) AS Total_Revenue,
        ROUND(SUM(t.Gross_Profit), 2) AS Total_Profit,
        DENSE_RANK() OVER (
            PARTITION BY p.Category 
            ORDER BY SUM(t.Total_Amount) DESC
        ) AS Category_Rank
    FROM starbucks_transactions t
    JOIN starbucks_products p ON t.Product_ID = p.Product_ID
    GROUP BY p.Category, p.Product_Name, p.Size
)
SELECT 
    Category,
    Category_Rank,
    Product_Name,
    Size,
    Total_Units_Sold,
    Total_Revenue,
    Total_Profit
FROM ProductPerformance
WHERE Category_Rank <= 3
ORDER BY Category, Category_Rank;


-- -------------------------------------------------------------------------------------
-- 3. MONTH-OVER-MONTH (MoM) AND YEAR-OVER-YEAR (YoY) SALES TRENDS (LAG WINDOW FUNCTION)
-- Tracks top-line revenue momentum and seasonality across consecutive quarters.
-- -------------------------------------------------------------------------------------
WITH MonthlySales AS (
    SELECT 
        d.Year,
        d.Month_Number,
        d.Month_Name,
        ROUND(SUM(t.Total_Amount), 2) AS Monthly_Revenue,
        COUNT(DISTINCT t.Transaction_ID) AS Monthly_Orders
    FROM starbucks_transactions t
    JOIN dim_date d ON t.Date = d.Date
    GROUP BY d.Year, d.Month_Number, d.Month_Name
),
SalesWithLags AS (
    SELECT 
        Year,
        Month_Number,
        Month_Name,
        Monthly_Revenue,
        Monthly_Orders,
        LAG(Monthly_Revenue, 1) OVER (ORDER BY Year, Month_Number) AS Prior_Month_Revenue,
        LAG(Monthly_Revenue, 12) OVER (ORDER BY Year, Month_Number) AS Prior_Year_Revenue
    FROM MonthlySales
)
SELECT 
    Year,
    Month_Name,
    Monthly_Revenue,
    Monthly_Orders,
    ROUND(((Monthly_Revenue - Prior_Month_Revenue) / NULLIF(Prior_Month_Revenue, 0)) * 100, 2) AS MoM_Growth_Pct,
    ROUND(((Monthly_Revenue - Prior_Year_Revenue) / NULLIF(Prior_Year_Revenue, 0)) * 100, 2) AS YoY_Growth_Pct
FROM SalesWithLags
ORDER BY Year, Month_Number;


-- -------------------------------------------------------------------------------------
-- 4. CAFFEINE PRICING EFFICIENCY & VALUE MATRIX
-- Measures cost-per-mg of caffeine across beverage lines to inform value-oriented menu pricing.
-- -------------------------------------------------------------------------------------
SELECT 
    p.Product_ID,
    p.Product_Name,
    p.Category,
    p.Size,
    p.Caffeine_mg,
    p.Unit_Price,
    CASE 
        WHEN p.Caffeine_mg > 0 THEN ROUND((p.Unit_Price / p.Caffeine_mg) * 100, 3)
        ELSE NULL 
    END AS Price_Cents_Per_Mg_Caffeine,
    CASE
        WHEN p.Caffeine_mg >= 200 THEN 'High Caffeine (200mg+)'
        WHEN p.Caffeine_mg BETWEEN 100 AND 199 THEN 'Moderate (100-199mg)'
        WHEN p.Caffeine_mg BETWEEN 1 AND 99 THEN 'Low (1-99mg)'
        ELSE 'Caffeine Free'
    END AS Caffeine_Bracket,
    COUNT(t.Transaction_ID) AS Volume_Purchased
FROM starbucks_products p
LEFT JOIN starbucks_transactions t ON p.Product_ID = t.Product_ID
WHERE p.Category != 'Bakery & Food'
GROUP BY p.Product_ID, p.Product_Name, p.Category, p.Size, p.Caffeine_mg, p.Unit_Price
ORDER BY Volume_Purchased DESC;


-- -------------------------------------------------------------------------------------
-- 5. STORE FORMAT & REAL ESTATE EFFICIENCY (REVENUE PER SQ FT)
-- Evaluates Drive-Thru vs. Street Front vs. Airport stores to guide future expansion CAPEX.
-- -------------------------------------------------------------------------------------
SELECT 
    s.Store_Type,
    COUNT(DISTINCT s.Store_ID) AS Store_Count,
    SUM(s.Sq_Footage) AS Total_Sq_Footage,
    ROUND(SUM(t.Total_Amount), 2) AS Total_Revenue,
    ROUND(SUM(t.Gross_Profit), 2) AS Total_Gross_Profit,
    ROUND(SUM(t.Total_Amount) / NULLIF(SUM(s.Sq_Footage), 0), 2) AS Revenue_Per_Sq_Ft,
    ROUND(AVG(t.Total_Amount), 2) AS Avg_Ticket_Size,
    ROUND((SUM(CASE WHEN t.Order_Channel = 'Mobile Order & Pay' THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 1) AS Mobile_Order_Pct
FROM starbucks_stores s
JOIN starbucks_transactions t ON s.Store_ID = t.Store_ID
GROUP BY s.Store_Type
ORDER BY Revenue_Per_Sq_Ft DESC;


-- -------------------------------------------------------------------------------------
-- 6. CUSTOMER RFM SEGMENTATION (RECENCY, FREQUENCY, MONETARY)
-- Segments customer base into Champions, Loyalists, At Risk, and Hibernating tiers.
-- -------------------------------------------------------------------------------------
WITH CustomerSummary AS (
    SELECT 
        Customer_ID,
        MAX(Date) AS Last_Purchase_Date,
        COUNT(DISTINCT Transaction_ID) AS Frequency,
        ROUND(SUM(Total_Amount), 2) AS Monetary
    FROM starbucks_transactions
    GROUP BY Customer_ID
),
RFMScores AS (
    SELECT 
        Customer_ID,
        Frequency,
        Monetary,
        NTILE(4) OVER (ORDER BY Last_Purchase_Date ASC) AS R_Score,
        NTILE(4) OVER (ORDER BY Frequency ASC) AS F_Score,
        NTILE(4) OVER (ORDER BY Monetary ASC) AS M_Score
    FROM CustomerSummary
)
SELECT 
    Customer_ID,
    Frequency,
    Monetary,
    R_Score,
    F_Score,
    M_Score,
    CASE 
        WHEN R_Score >= 3 AND F_Score >= 3 AND M_Score >= 3 THEN 'Champion'
        WHEN F_Score >= 3 AND M_Score >= 2 THEN 'Loyal Customer'
        WHEN R_Score <= 2 AND F_Score >= 3 THEN 'At Risk (High Value Inactive)'
        WHEN R_Score <= 2 AND F_Score <= 2 THEN 'Hibernating / Churned'
        ELSE 'Potential Loyalist'
    END AS Customer_Segment
FROM RFMScores
ORDER BY Monetary DESC
LIMIT 50;


-- -------------------------------------------------------------------------------------
-- 7. PEAK HOURLY DEMAND & CHANNEL AFFINITY
-- Optimizes store labor scheduling across morning commute (7-9 AM) and afternoon lull.
-- -------------------------------------------------------------------------------------
SELECT 
    t.Hour,
    COUNT(t.Transaction_ID) AS Total_Orders,
    ROUND(SUM(t.Total_Amount), 2) AS Total_Revenue,
    ROUND(AVG(t.Total_Amount), 2) AS Avg_Order_Value,
    ROUND(SUM(CASE WHEN t.Order_Channel = 'Drive-Thru' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS Drive_Thru_Pct,
    ROUND(SUM(CASE WHEN t.Order_Channel = 'Mobile Order & Pay' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS Mobile_Pay_Pct,
    ROUND(SUM(CASE WHEN t.Order_Channel = 'In-Store' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS In_Store_Pct
FROM starbucks_transactions t
GROUP BY t.Hour
ORDER BY t.Hour ASC;
