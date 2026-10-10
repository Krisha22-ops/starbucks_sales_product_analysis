# Starbucks Sales & Product Analytics - Star Schema Data Model

## Architecture Overview
The Power BI semantic model is structured as a pure **Star Schema** to optimize query performance via the VertiPaq engine, avoid bi-directional relationship ambiguity, and ensure seamless DAX filter context propagation.

```mermaid
erDiagram
    Dim_Date ||--o{ Fact_Transactions : "Date = Date (1:*)"
    Dim_Product ||--o{ Fact_Transactions : "Product_ID = Product_ID (1:*)"
    Dim_Store ||--o{ Fact_Transactions : "Store_ID = Store_ID (1:*)"

    Fact_Transactions {
        string Transaction_ID PK
        datetime Timestamp
        string Date FK
        int Hour
        string Customer_ID
        string Store_ID FK
        string Product_ID FK
        int Quantity
        float Unit_Price
        float Subtotal
        float Discount_Amount
        float Total_Amount
        float Total_Cost
        float Gross_Profit
        string Payment_Method
        string Order_Channel
        int Is_Loyalty_Member
    }

    Dim_Product {
        string Product_ID PK
        string Category
        string Product_Name
        string Size
        string Milk_Type
        int Calories
        float Fat_g
        int Carb_g
        int Protein_g
        int Caffeine_mg
        float Unit_Price
        float Unit_Cost
        float Gross_Margin
        float Gross_Margin_Pct
    }

    Dim_Store {
        string Store_ID PK
        string Store_Name
        string City
        string State
        string Store_Type
        int Sq_Footage
        string Region
    }

    Dim_Date {
        string Date PK
        int Year
        string Quarter
        string Month_Name
        int Month_Number
        int Day
        string Day_Of_Week
        int Is_Weekend
    }
```

---

## Relationship Configuration Matrix

| From Table (Dimension) | Primary Key | To Table (Fact) | Foreign Key | Cardinality | Cross Filter Direction | Active |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| `Dim_Product` | `Product_ID` | `Fact_Transactions` | `Product_ID` | `1 : Many (*)` | Single (Dim -> Fact) | Yes |
| `Dim_Store` | `Store_ID` | `Fact_Transactions` | `Store_ID` | `1 : Many (*)` | Single (Dim -> Fact) | Yes |
| `Dim_Date` | `Date` | `Fact_Transactions` | `Date` | `1 : Many (*)` | Single (Dim -> Fact) | Yes |

---

## VertiPaq Storage Engine Optimization Highlights
1. **Explicit Star Schema**: Eliminated snowflake normalization to avoid snowflake join penalties.
2. **Surrogate Keys**: Integer-like and compact alphanumeric IDs (`PRD_001`, `STR_001`) reduce column cardinality and memory footprint.
3. **Column Splitting**: Split high-cardinality `Timestamp` into `Date` (FK to `Dim_Date`) and `Hour` integer (0 to 23), reducing dictionary size from 15,000 distinct strings to 731 dates + 24 hours.
4. **Calculated Measures vs Columns**: All dynamic KPIs (AOV, Gross Margin %, YoY Growth) are built as explicit DAX measures rather than calculated columns to minimize disk and RAM footprint.
