import pandas as pd

# Load raw dataset
file_path = r"D:\DVP_Ecommerce_Project\Dataset\Global_Superstore.csv"

df = pd.read_csv(file_path)

print("========== DATA CLEANING ==========")

# Convert date columns to datetime
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

# Handle missing Postal Code values
df["Postal Code"] = df["Postal Code"].fillna(0)

# Remove duplicate rows
df = df.drop_duplicates()

# Remove rows with missing important values
important_columns = [
    "Order ID",
    "Customer ID",
    "Product ID",
    "Sales",
    "Profit"
]

df = df.dropna(subset=important_columns)

# Sort data by Order Date
df = df.sort_values("Order Date")

# Reset index
df = df.reset_index(drop=True)

# Save cleaned dataset
output_path = r"D:\DVP_Ecommerce_Project\Dataset\Global_Superstore_Cleaned.csv"

df.to_csv(output_path, index=False)

print("\nData cleaning completed successfully!")

print("\nCleaned dataset shape:")
print(df.shape)

print("\nRemaining missing values:")
print(df.isnull().sum())

print("\nCleaned dataset saved to:")
print(output_path)