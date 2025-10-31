#Generates line, bar, and pie charts for data visualization.
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    try:
        df = pd.read_csv("transactions.csv")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        return df
    except FileNotFoundError:
        print("No transaction file found.")
        return pd.DataFrame(columns=["Date", "Category", "Description", "Amount", "Type", "NeedOrWant"])

#1. Monthly Spending Trend (Line Chart)
def monthly_spending_trend(df):
    expenses = df[df["Type"].str.lower() == "expense"].copy()
    if expenses.empty:
        print("\nNo expense data found for visualization.")
        return

    expenses["Month"] = expenses["Date"].dt.to_period("M")
    monthly_sum = expenses.groupby("Month")["Amount"].sum()

    plt.figure(figsize=(8, 5))
    plt.plot(monthly_sum.index.astype(str), monthly_sum.values, marker='o', linewidth=2)
    plt.title("📅 Monthly Spending Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Spending ($)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#2. Spending by Category (Bar Chart)
def spending_by_category(df):
    expenses = df[df["Type"].str.lower() == "expense"]
    if expenses.empty:
        print("\nNo expense data found for visualization.")
        return

    expenses["Category"] = expenses["Category"].str.title()
    category_sum = expenses.groupby("Category")["Amount"].sum().sort_values(ascending=False)

    plt.figure(figsize=(8, 5))
    category_sum.plot(kind="bar", color="skyblue", edgecolor="black")
    plt.title("💰 Spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Amount ($)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

#3. Percentage Distribution (Pie Chart)
def percentage_distribution(df):
    expenses = df[df["Type"].str.lower() == "expense"]
    if expenses.empty:
        print("\nNo expense data found for visualization.")
        return
    expenses["Category"] = expenses["Category"].str.title()
    category_sum = expenses.groupby("Category")["Amount"].sum()

    plt.figure(figsize=(6, 6))
    plt.pie(category_sum, labels=category_sum.index, autopct="%1.1f%%", startangle=90)
    plt.title("🍩 Percentage Distribution of Spending by Category")
    plt.tight_layout()
    plt.show()

def show_charts():
    df = load_data()
    if df.empty:
        print("\nNo transactions found for visualization.")
        return

    while True:
        print("\n==== Data Visualization Menu ====")
        print("1. Monthly Spending Trend (Line Chart)")
        print("2. Spending by Category (Bar Chart)")
        print("3. Percentage Distribution (Pie Chart)")
        print("4. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            monthly_spending_trend(df)
        elif choice == '2':
            spending_by_category(df)
        elif choice == '3':
            percentage_distribution(df)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")