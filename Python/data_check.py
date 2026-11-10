import pandas as pd

# Load the dataset
file_path = r"D:\DVP_Ecommerce_Project\Dataset\Global_Superstore.csv"

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print()

print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

print()
print("Column names:")
print(df.columns.tolist())

print()
print("First 5 rows:")
print(df.head())
