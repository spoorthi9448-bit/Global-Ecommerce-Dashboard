from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)

CORS(app)

file_path = r"D:\DVP_Ecommerce_Project\Dataset\Global_Superstore_Cleaned.csv"
df = pd.read_csv(file_path)

# Convert dates
df["Order Date"] = pd.to_datetime(df["Order Date"])


@app.route("/")
def home():
    return "E-Commerce Analytics Backend is running!"


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").lower().strip()

    if "total sales" in question:
        answer = f"Total sales are ${df['Sales'].sum():,.2f}."

    elif "total profit" in question:
        answer = f"Total profit is ${df['Profit'].sum():,.2f}."

    elif "profit margin" in question:
        margin = (df["Profit"].sum() / df["Sales"].sum()) * 100
        answer = f"The overall profit margin is {margin:.2f}%."

    elif "customers" in question:
        answer = f"There are {df['Customer ID'].nunique():,} unique customers."

    elif "orders" in question:
        answer = f"There are {df['Order ID'].nunique():,} unique orders."

    elif "region" in question and any(word in question for word in ["highest", "most", "top", "best"]) and "sales" in question:
        region_sales = df.groupby("Region")["Sales"].sum()
        region = region_sales.idxmax()
        sales = region_sales.max()
        answer = f"{region} has the highest sales with ${sales:,.2f}."

    elif "product" in question and any(word in question for word in ["highest", "most", "top", "best"]) and "sales" in question:
        product_sales = df.groupby("Product Name")["Sales"].sum()
        product = product_sales.idxmax()
        sales = product_sales.max()
        answer = f"{product} has the highest sales with ${sales:,.2f}."

    elif ("category" in question or "categories" in question) and any(word in question for word in ["highest", "maximum", "most", "top", "best"]) and any(word in question for word in ["sale", "sales", "revenue"]):
        category_sales = df.groupby("Category")["Sales"].sum()
        category = category_sales.idxmax()
        sales = category_sales.max()
        answer = f"{category} has the highest sales with ${sales:,.2f}."

    elif "category" in question and "profit" in question and any(word in question for word in ["highest", "maximum", "most", "top", "best"]):
        category_profit = df.groupby("Category")["Profit"].sum()
        category = category_profit.idxmax()
        profit = category_profit.max()
        answer = f"{category} has the highest profit with ${profit:,.2f}."

    elif "average order value" in question or "average order" in question:
        average_order_value = df["Sales"].sum() / df["Order ID"].nunique()
        answer = f"The average order value is ${average_order_value:,.2f}."

    else:
        answer = "I don't know that question yet. Try asking about sales, profit, customers, orders, regions, products, or categories."

    return jsonify({"answer": answer})
  
@app.route("/api/dashboard", methods=["GET"])
def dashboard_data():
    # Summary cards
    total_sales = float(df["Sales"].sum())
    total_profit = float(df["Profit"].sum())
    total_orders = int(df["Order ID"].nunique())
    total_customers = int(df["Customer ID"].nunique())

    # Sales by category
    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    # Profit by category
    category_profit = (
        df.groupby("Category")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    # Top 10 products by sales
    top_products = (
        df.groupby("Product Name")["Sales"]
        .sum()
        .nlargest(10)
    )

    # Sales by region
    region_sales = (
        df.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    # Sales, profit and orders by country
    country_sales = (
        df.groupby("Country")
        .agg(
            sales=("Sales", "sum"),
            profit=("Profit", "sum"),
            orders=("Order ID", "nunique")
        )
        .sort_values(by="sales", ascending=False)
    )

    # Monthly sales trend
    monthly_sales = (
        df.assign(Month=df["Order Date"].dt.to_period("M").astype(str))
        .groupby("Month")["Sales"]
        .sum()
        .sort_index()
    )

    return jsonify({
        "summary": {
            "total_sales": round(total_sales, 2),
            "total_profit": round(total_profit, 2),
            "total_orders": total_orders,
            "total_customers": total_customers,
            "average_order_value": round(
                total_sales / total_orders, 2
            ) if total_orders else 0
        },
        "category_sales": {
            "labels": category_sales.index.tolist(),
            "values": category_sales.tolist()
        },
        "category_profit": {
            "labels": category_profit.index.tolist(),
            "values": category_profit.tolist()
        },
        "top_products": {
            "labels": top_products.index.tolist(),
            "values": top_products.tolist()
        },
        "region_sales": {
            "labels": region_sales.index.tolist(),
            "values": region_sales.tolist()
        },
                "countries": [
    {
        "Country": country,
        "sales": float(row["sales"]),
        "profit": float(row["profit"]),
        "orders": int(row["orders"])
    }
    for country, row in country_sales.iterrows()
],
        "monthly_sales": {
            "labels": monthly_sales.index.tolist(),
            "values": monthly_sales.tolist()
        }
    })

    # ==========================================
# 8. COUNTRY-WISE DATA FOR INTERACTIVE GLOBE
# ==========================================

@app.route("/api/country", methods=["GET"])
def get_country_details():

    country = request.args.get("country", "").strip()

    if not country:
        return jsonify({"error": "Please provide a country name."}), 400

    country_df = df[
        df["Country"].str.strip().str.lower() == country.lower()
    ].copy()

    if country_df.empty:
        return jsonify({"error": "Country not found."}), 404

    # 1. SALES DETAILS
    summary = {
        "total_sales": round(float(country_df["Sales"].sum()), 2),
        "total_profit": round(float(country_df["Profit"].sum()), 2),
        "total_quantity": int(country_df["Quantity"].sum()),
        "total_orders": int(country_df["Order ID"].nunique()),
        "total_customers": int(country_df["Customer ID"].nunique())
    }

    # 2. CATEGORY DETAILS
    categories = (
        country_df.groupby("Category")
        .agg(
            sales=("Sales", "sum"),
            profit=("Profit", "sum"),
            quantity=("Quantity", "sum")
        )
        .reset_index()
        .sort_values("sales", ascending=False)
    )

    # 3. PRODUCT DETAILS - ALL PRODUCTS
    products = (
        country_df.groupby("Product Name")
        .agg(
            sales=("Sales", "sum"),
            profit=("Profit", "sum"),
            quantity=("Quantity", "sum")
        )
        .reset_index()
        .sort_values("sales", ascending=False)
    )

    # 4. TOP 10 PRODUCTS
    top_products = products.head(10)

    # 5. CUSTOMER DETAILS
    customers = (
        country_df.groupby(["Customer ID", "Customer Name"])
        .agg(
            orders=("Order ID", "nunique"),
            sales=("Sales", "sum"),
            profit=("Profit", "sum")
        )
        .reset_index()
        .sort_values("sales", ascending=False)
    )

    # 6. ORDER DETAILS
    order_columns = [
        "Order ID",
        "Order Date",
        "Ship Date",
        "Ship Mode",
        "Customer ID",
        "Customer Name"
    ]

    order_columns = [
        col for col in order_columns if col in country_df.columns
    ]

    orders = (
        country_df.groupby("Order ID")
        .agg({
            **{col: "first" for col in order_columns if col != "Order ID"},
            "Sales": "sum",
            "Profit": "sum",
            "Quantity": "sum"
        })
        .reset_index()
    )

    for col in ["Order Date", "Ship Date"]:
        if col in orders.columns:
            orders[col] = orders[col].astype(str)

    # 7. COUNTRY REGION
    region = country_df["Region"].iloc[0]

    return jsonify({
        "country": country_df["Country"].iloc[0],
        "region": region,
        "summary": summary,
        "categories": categories.to_dict(orient="records"),
        "products": products.to_dict(orient="records"),
        "top_products": top_products.to_dict(orient="records"),
        "customers": customers.to_dict(orient="records"),
        "orders": orders.to_dict(orient="records")
    })
if __name__ == "__main__":
    app.run(debug=True)