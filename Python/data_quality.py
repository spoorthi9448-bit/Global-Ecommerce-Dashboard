import pandas as pd

# Load the dataset
file_path = r"D:\DVP_Ecommerce_Project\Dataset\Global_Superstore.csv"

df = pd.read_csv(file_path)

print("========== DATA QUALITY CHECK ==========")

# 1. Dataset shape
print("\n1. Dataset Shape:")
print(df.shape)

# 2. Missing values
print("\n2. Missing Values:")
print(df.isnull().sum())

# 3. Duplicate rows
print("\n3. Duplicate Rows:")
print(df.duplicated().sum())

# 4. Data types
print("\n4. Data Types:")
print(df.dtypes)

# 5. Basic statistics
print("\n5. Numerical Summary:")
print(df.describe())