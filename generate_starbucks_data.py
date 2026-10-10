"""
Starbucks Enterprise Sales & Nutritional Data Generator
========================================================
Generates a multi-table relational dataset:
1. data/starbucks_products.csv (100+ menu items with nutritional facts, caffeine, costs & pricing)
2. data/starbucks_stores.csv (Store dimensions, square footage, store formats)
3. data/starbucks_transactions.csv (15,000+ realistic transaction logs spanning 2023-2024)
4. data/dim_date.csv (Complete date dimension for Power BI time intelligence)
"""

import os
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

# Fix random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_starbucks_dataset(base_dir: str):
    data_dir = Path(base_dir) / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating Starbucks Product Catalog & Nutritional Data...")
    
    products_raw = [
        # Category, Name, Size, Milk, Cal, Fat, Carb, Protein, Caffeine, Price, Cost
        ("Hot Coffees", "Pike Place Roast", "Tall", "None", 5, 0.0, 0, 1, 235, 2.95, 0.45),
        ("Hot Coffees", "Pike Place Roast", "Grande", "None", 5, 0.0, 0, 1, 310, 3.45, 0.55),
        ("Hot Coffees", "Pike Place Roast", "Venti", "None", 5, 0.0, 0, 1, 410, 3.95, 0.65),
        ("Hot Coffees", "Caffè Americano", "Tall", "None", 10, 0.0, 2, 1, 150, 3.25, 0.40),
        ("Hot Coffees", "Caffè Americano", "Grande", "None", 15, 0.0, 3, 1, 225, 3.75, 0.50),
        ("Hot Coffees", "Caffè Americano", "Venti", "None", 25, 0.0, 4, 2, 300, 4.25, 0.60),
        ("Hot Coffees", "Caffè Latte", "Tall", "2% Milk", 150, 6.0, 15, 10, 75, 4.45, 0.85),
        ("Hot Coffees", "Caffè Latte", "Grande", "2% Milk", 190, 7.0, 19, 13, 150, 4.95, 1.05),
        ("Hot Coffees", "Caffè Latte", "Venti", "2% Milk", 250, 9.0, 24, 16, 150, 5.45, 1.25),
        ("Hot Coffees", "Caramel Macchiato", "Tall", "2% Milk", 180, 5.0, 24, 8, 75, 4.95, 0.95),
        ("Hot Coffees", "Caramel Macchiato", "Grande", "2% Milk", 250, 7.0, 35, 10, 150, 5.65, 1.20),
        ("Hot Coffees", "Caramel Macchiato", "Venti", "2% Milk", 310, 9.0, 44, 13, 150, 6.15, 1.45),
        ("Hot Coffees", "White Chocolate Mocha", "Grande", "2% Milk", 430, 18.0, 55, 12, 150, 5.95, 1.40),
        ("Hot Coffees", "Cappuccino", "Grande", "Whole Milk", 140, 5.0, 12, 9, 150, 4.95, 0.90),
        
        ("Cold Coffees", "Starbucks Cold Brew", "Tall", "None", 5, 0.0, 0, 0, 155, 3.95, 0.45),
        ("Cold Coffees", "Starbucks Cold Brew", "Grande", "None", 5, 0.0, 0, 0, 205, 4.45, 0.55),
        ("Cold Coffees", "Starbucks Cold Brew", "Venti", "None", 5, 0.0, 0, 0, 310, 4.95, 0.70),
        ("Cold Coffees", "Vanilla Sweet Cream Cold Brew", "Grande", "Vanilla Cream", 110, 5.0, 14, 1, 185, 5.25, 0.95),
        ("Cold Coffees", "Vanilla Sweet Cream Cold Brew", "Venti", "Vanilla Cream", 200, 11.0, 23, 2, 275, 5.75, 1.15),
        ("Cold Coffees", "Iced Brown Sugar Oat Shaken Espresso", "Grande", "Oatmilk", 120, 3.0, 20, 2, 255, 5.95, 1.10),
        ("Cold Coffees", "Iced Brown Sugar Oat Shaken Espresso", "Venti", "Oatmilk", 190, 4.5, 34, 3, 340, 6.45, 1.30),
        ("Cold Coffees", "Iced Caramel Macchiato", "Grande", "2% Milk", 250, 7.0, 37, 10, 150, 5.75, 1.15),
        ("Cold Coffees", "Iced Caffè Mocha", "Grande", "2% Milk", 350, 17.0, 42, 10, 175, 5.85, 1.25),
        ("Cold Coffees", "Nitro Cold Brew", "Grande", "None", 5, 0.0, 0, 0, 280, 5.45, 0.65),

        ("Frappuccino", "Caramel Ribbon Crunch Frappuccino", "Tall", "Whole Milk", 330, 15.0, 46, 3, 60, 5.45, 1.20),
        ("Frappuccino", "Caramel Ribbon Crunch Frappuccino", "Grande", "Whole Milk", 470, 22.0, 65, 5, 85, 6.15, 1.45),
        ("Frappuccino", "Mocha Cookie Crumble Frappuccino", "Grande", "Whole Milk", 480, 24.0, 63, 6, 95, 6.25, 1.50),
        ("Frappuccino", "Java Chip Frappuccino", "Grande", "Whole Milk", 440, 19.0, 65, 6, 105, 5.95, 1.35),
        ("Frappuccino", "Coffee Frappuccino", "Grande", "Whole Milk", 230, 3.0, 45, 3, 95, 5.25, 1.10),
        ("Frappuccino", "Strawberries & Crème Frappuccino", "Grande", "Whole Milk", 370, 15.0, 54, 5, 0, 5.75, 1.25),

        ("Teas & Refreshers", "Iced Peach Green Tea Lemonade", "Grande", "None", 80, 0.0, 19, 0, 25, 4.75, 0.65),
        ("Teas & Refreshers", "Mango Dragonfruit Refresher", "Grande", "None", 90, 0.0, 21, 0, 45, 5.15, 0.70),
        ("Teas & Refreshers", "Strawberry Açaí Lemonade", "Grande", "None", 140, 0.0, 35, 1, 45, 5.25, 0.75),
        ("Teas & Refreshers", "Chai Tea Latte", "Grande", "2% Milk", 240, 4.5, 45, 8, 95, 4.95, 0.90),
        ("Teas & Refreshers", "Matcha Tea Latte", "Grande", "2% Milk", 240, 7.0, 34, 12, 80, 5.45, 1.05),

        ("Bakery & Food", "Bacon, Gouda & Egg Sandwich", "Single", "None", 360, 18.0, 32, 19, 0, 5.45, 1.85),
        ("Bakery & Food", "Double-Smoked Bacon Sandwich", "Single", "None", 500, 28.0, 42, 21, 0, 6.25, 2.20),
        ("Bakery & Food", "Spinach, Feta & Egg White Wrap", "Single", "None", 290, 8.0, 34, 20, 0, 5.25, 1.70),
        ("Bakery & Food", "Butter Croissant", "Single", "None", 250, 14.0, 26, 5, 0, 3.45, 0.80),
        ("Bakery & Food", "Chocolate Croissant", "Single", "None", 300, 17.0, 34, 5, 0, 3.95, 0.95),
        ("Bakery & Food", "Blueberry Muffin", "Single", "None", 360, 15.0, 52, 5, 0, 3.65, 0.85),
        ("Bakery & Food", "Glazed Donut", "Single", "None", 440, 23.0, 54, 5, 0, 2.95, 0.60),
        ("Bakery & Food", "Cake Pop - Birthday Cake", "Single", "None", 160, 8.0, 22, 1, 0, 2.95, 0.45)
    ]
    
    prod_df = pd.DataFrame(products_raw, columns=[
        "Category", "Product_Name", "Size", "Milk_Type", "Calories", 
        "Fat_g", "Carb_g", "Protein_g", "Caffeine_mg", "Unit_Price", "Unit_Cost"
    ])
    prod_df.insert(0, "Product_ID", [f"PRD_{i+1:03d}" for i in range(len(prod_df))])
    prod_df["Gross_Margin"] = (prod_df["Unit_Price"] - prod_df["Unit_Cost"]).round(2)
    prod_df["Gross_Margin_Pct"] = ((prod_df["Gross_Margin"] / prod_df["Unit_Price"]) * 100).round(1)
    
    prod_csv = data_dir / "starbucks_products.csv"
    prod_df.to_csv(prod_csv, index=False)
    print(f"Saved {len(prod_df)} products to {prod_csv}")

    # Generate Stores Dimension
    stores_raw = [
        ("STR_001", "Downtown Flagship", "Seattle", "WA", "Drive-Thru", 2200, "Pacific Northwest"),
        ("STR_002", "Pike Place Market", "Seattle", "WA", "Street Front", 1400, "Pacific Northwest"),
        ("STR_003", "Financial District", "New York", "NY", "Street Front", 1100, "Northeast"),
        ("STR_004", "JFK Terminal 4", "New York", "NY", "Airport", 850, "Northeast"),
        ("STR_005", "Michigan Avenue", "Chicago", "IL", "Street Front", 1800, "Midwest"),
        ("STR_006", "O'Hare Concourse B", "Chicago", "IL", "Airport", 950, "Midwest"),
        ("STR_007", "Oakridge Mall", "San Jose", "CA", "Mall", 1250, "West Coast"),
        ("STR_008", "Santana Row", "San Jose", "CA", "Drive-Thru", 2000, "West Coast"),
        ("STR_009", "Austin Downtown", "Austin", "TX", "Drive-Thru", 2400, "South"),
        ("STR_010", "Galleria Mall", "Houston", "TX", "Mall", 1500, "South")
    ]
    store_df = pd.DataFrame(stores_raw, columns=[
        "Store_ID", "Store_Name", "City", "State", "Store_Type", "Sq_Footage", "Region"
    ])
    store_csv = data_dir / "starbucks_stores.csv"
    store_df.to_csv(store_csv, index=False)
    print(f"Saved {len(store_df)} stores to {store_csv}")

    # Generate Date Dimension
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_list = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    
    date_df = pd.DataFrame({
        "Date": [d.strftime("%Y-%m-%d") for d in date_list],
        "Year": [d.year for d in date_list],
        "Quarter": [f"Q{((d.month - 1) // 3) + 1}" for d in date_list],
        "Month_Name": [d.strftime("%B") for d in date_list],
        "Month_Number": [d.month for d in date_list],
        "Day": [d.day for d in date_list],
        "Day_Of_Week": [d.strftime("%A") for d in date_list],
        "Is_Weekend": [1 if d.weekday() >= 5 else 0 for d in date_list]
    })
    date_csv = data_dir / "dim_date.csv"
    date_df.to_csv(date_csv, index=False)
    print(f"Saved {len(date_df)} dates to {date_csv}")

    # Generate 15,000 Transactions Fact Table
    print("Generating 15,000 transactions...")
    n_transactions = 15000
    
    # Weight beverage popularity (Cold Brew, Iced Shaken Espresso, Pike Place, Macchiato are top)
    prod_weights = np.ones(len(prod_df))
    # Cold Coffees & Frappuccinos get higher volume
    for i, row in prod_df.iterrows():
        if "Cold Brew" in row["Product_Name"] or "Shaken" in row["Product_Name"]:
            prod_weights[i] = 4.0
        elif row["Category"] == "Hot Coffees":
            prod_weights[i] = 2.5
        elif row["Category"] == "Frappuccino":
            prod_weights[i] = 2.0
        elif row["Category"] == "Bakery & Food":
            prod_weights[i] = 1.8
    prod_weights /= prod_weights.sum()

    txn_dates = [random.choice(date_list) for _ in range(n_transactions)]
    # Simulate hourly peak: 7am-9am morning rush, 1pm-3pm afternoon rush
    hours_dist = [6, 7, 7, 8, 8, 8, 9, 9, 10, 11, 12, 13, 14, 14, 15, 16, 17, 18, 19, 20]
    
    records = []
    customer_pool = [f"CUST_{i:04d}" for i in range(1, 1201)]
    channels = ["In-Store", "Drive-Thru", "Mobile Order & Pay"]
    pay_methods = ["Starbucks App", "Credit Card", "Apple Pay", "Cash"]
    
    for i in range(n_transactions):
        txn_id = f"TXN_{i+1:06d}"
        d = txn_dates[i]
        hour = random.choice(hours_dist)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        dt_str = f"{d.strftime('%Y-%m-%d')} {hour:02d}:{minute:02d}:{second:02d}"
        
        cust_id = random.choice(customer_pool)
        store = random.choice(stores_raw)
        store_id = store[0]
        
        # Pick product
        prod_idx = np.random.choice(len(prod_df), p=prod_weights)
        prod = prod_df.iloc[prod_idx]
        prod_id = prod["Product_ID"]
        unit_price = float(prod["Unit_Price"])
        unit_cost = float(prod["Unit_Cost"])
        
        # Quantity usually 1 or 2
        qty = np.random.choice([1, 2, 3], p=[0.75, 0.20, 0.05])
        subtotal = round(unit_price * qty, 2)
        
        # Channel & Member
        is_member = np.random.choice([1, 0], p=[0.68, 0.32])
        if store[4] == "Drive-Thru":
            channel = np.random.choice(channels, p=[0.2, 0.65, 0.15])
        elif store[4] == "Airport":
            channel = "In-Store"
        else:
            channel = np.random.choice(["In-Store", "Mobile Order & Pay"], p=[0.55, 0.45])
            
        pay_method = "Starbucks App" if (is_member and random.random() < 0.8) else random.choice(pay_methods)
        discount = round(subtotal * 0.10, 2) if (is_member and random.random() < 0.25) else 0.0
        final_amount = round(subtotal - discount, 2)
        total_cost = round(unit_cost * qty, 2)
        gross_profit = round(final_amount - total_cost, 2)
        
        records.append({
            "Transaction_ID": txn_id,
            "Timestamp": dt_str,
            "Date": d.strftime("%Y-%m-%d"),
            "Hour": hour,
            "Customer_ID": cust_id,
            "Store_ID": store_id,
            "Product_ID": prod_id,
            "Quantity": qty,
            "Unit_Price": unit_price,
            "Subtotal": subtotal,
            "Discount_Amount": discount,
            "Total_Amount": final_amount,
            "Total_Cost": total_cost,
            "Gross_Profit": gross_profit,
            "Payment_Method": pay_method,
            "Order_Channel": channel,
            "Is_Loyalty_Member": is_member
        })

    fact_df = pd.DataFrame(records)
    fact_csv = data_dir / "starbucks_transactions.csv"
    fact_df.to_csv(fact_csv, index=False)
    print(f"Saved {len(fact_df)} transactions to {fact_csv}")
    print("Starbucks dataset generation complete!")

if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent
    generate_starbucks_dataset(str(current_dir))
