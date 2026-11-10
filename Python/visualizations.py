import pandas as pd
import matplotlib.pyplot as plt
import os

# Load cleaned dataset
file_path = r"D:\DVP_Ecommerce_Project\Dataset\Global_Superstore_Cleaned.csv"

df = pd.read_csv(file_path)

# Convert Order Date
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Create visualization folder if it doesn't exist
output_folder = r"D:\DVP_Ecommerce_Project\Visualizations"
os.makedirs(output_folder, exist_ok=True)


# ==========================================
# 1. SALES BY CATEGORY
# ==========================================

sales_by_category = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
sales_by_category.plot(kind="bar")

plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    os.path.join(output_folder, "Sales_by_Category.png"),
    dpi=300
)

plt.show()


# ==========================================
# 2. PROFIT BY CATEGORY
# ==========================================

profit_by_category = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
profit_by_category.plot(kind="bar")

plt.title("Profit by Category")
plt.xlabel("Category")
plt.ylabel("Profit")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    os.path.join(output_folder, "Profit_by_Category.png"),
    dpi=300
)

plt.show()


# ==========================================
# 3. SALES BY REGION
# ==========================================

sales_by_region = df.groupby("Region")["Sales"].sum().sort_values(ascending=True)

plt.figure(figsize=(10, 8))
sales_by_region.plot(kind="barh")

plt.title("Sales by Region")
plt.xlabel("Sales")
plt.ylabel("Region")
plt.tight_layout()

plt.savefig(
    os.path.join(output_folder, "Sales_by_Region.png"),
    dpi=300
)

plt.show()


# ==========================================
# 4. TOP 10 PRODUCTS
# ==========================================

top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values(ascending=True)
)

plt.figure(figsize=(10, 7))
top_products.plot(kind="barh")

plt.title("Top 10 Products by Sales")
plt.xlabel("Sales")
plt.ylabel("Product")
plt.tight_layout()

plt.savefig(
    os.path.join(output_folder, "Top_10_Products.png"),
    dpi=300
)

plt.show()


# ==========================================
# 5. MONTHLY SALES TREND
# ==========================================

monthly_sales = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
    .sum()
)

monthly_sales.index = monthly_sales.index.astype(str)

plt.figure(figsize=(12, 6))
plt.plot(monthly_sales.index, monthly_sales.values, marker="o")

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=90)
plt.tight_layout()

plt.savefig(
    os.path.join(output_folder, "Monthly_Sales_Trend.png"),
    dpi=300
)

plt.show()


print("\n======================================")
print("ALL VISUALIZATIONS CREATED SUCCESSFULLY")
print("======================================")

print("\nSaved in:")
print(output_folder)