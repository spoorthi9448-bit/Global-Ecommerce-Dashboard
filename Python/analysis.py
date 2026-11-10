import pandas as pd

# Load cleaned dataset
file_path = r"D:\DVP_Ecommerce_Project\Dataset\Global_Superstore_Cleaned.csv"

df = pd.read_csv(file_path)

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# ==============================
# KEY BUSINESS METRICS
# ==============================

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()
total_customers = df["Customer ID"].nunique()
total_products = df["Product ID"].nunique()

average_order_value = total_sales / total_orders
profit_margin = (total_profit / total_sales) * 100

# ==============================
# DISPLAY RESULTS
# ==============================

print("======================================")
print(" GLOBAL E-COMMERCE ANALYSIS")
print("======================================")

print(f"\nTotal Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Customers: {total_customers:,}")
print(f"Total Products: {total_products:,}")
print(f"Average Order Value: ${average_order_value:,.2f}")
print(f"Profit Margin: {profit_margin:.2f}%")

# ==============================
# SALES BY CATEGORY
# ==============================

print("\n======================================")
print(" SALES BY CATEGORY")
print("======================================")

sales_by_category = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(sales_by_category)

# ==============================
# PROFIT BY CATEGORY
# ==============================

print("\n======================================")
print(" PROFIT BY CATEGORY")
print("======================================")

profit_by_category = (
    df.groupby("Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print(profit_by_category)

# ==============================
# SALES BY REGION
# ==============================

print("\n======================================")
print(" SALES BY REGION")
print("======================================")

sales_by_region = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print(sales_by_region)

# ==============================
# TOP 10 PRODUCTS
# ==============================

print("\n======================================")
print(" TOP 10 PRODUCTS BY SALES")
print("======================================")

top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_products)

# ==============================
# MONTHLY SALES
# ==============================

print("\n======================================")
print(" MONTHLY SALES")
print("======================================")

monthly_sales = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
)

print(monthly_sales)