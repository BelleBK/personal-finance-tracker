#Analyzes spending by category, calculates average spending, and identifies top spending categories.
import pandas as pd
def load_data():
    try:
        df = pd.read_csv("transactions.csv")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        return df
    except FileNotFoundError:
        print("No transaction file found.")
        return pd.DataFrame(columns=["Date", "Category", "Description", "Amount", "Type", "NeedOrWant"])

#1. Analyze Spending by Category
def analyze_by_category(df):
    expenses = df[df["Type"].str.lower() == "expense"]
    if expenses.empty:
        print("\nNo expense transactions found.")
        return

    category_summary = expenses.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    print("\n💰 Total Spending by Category:")
    print(category_summary)
    print("----------------------------------")

#2. Calculate Average Monthly Spending
def average_monthly_spending(df):
    expenses = df[df["Type"].str.lower() == "expense"].copy()
    if expenses.empty:
        print("\nNo expense transactions found.")
        return

    expenses["Month"] = expenses["Date"].dt.to_period("M")
    monthly_sum = expenses.groupby("Month")["Amount"].sum()
    avg_spending = monthly_sum.mean()

    print("\n📅 Average Monthly Spending:")
    print(monthly_sum)
    print(f"\nAverage spending per month: ${avg_spending:.2f}")
    print("----------------------------------")

#3. Show Top Spending Category
def top_spending_category(df):
    expenses = df[df["Type"].str.lower() == "expense"]
    if expenses.empty:
        print("\nNo expense transactions found.")
        return

    totals = expenses.groupby("Category")["Amount"].sum()
    top_cat = totals.idxmax()
    top_value = totals.max()

    print(f"\n🏆 Top Spending Category: {top_cat} (${top_value:.2f})")
    print("----------------------------------")

#4. Show Top Spending Category by month
def top_category_by_month(df):
    expenses = df[df["Type"].str.lower() == "expense"].copy()
    if expenses.empty:
        print("\nNo expense transactions found.")
        return

    expenses["Month"] = expenses["Date"].dt.to_period("M")
    print("\n📆 Top Spending Category by Month:")

    for month, data in expenses.groupby("Month"):
        category_totals = data.groupby("Category")["Amount"].sum()
        if category_totals.empty:
            print(f"{month}: No expenses recorded.")
        else:
            top_cat = category_totals.idxmax()
            top_val = category_totals.max()
            print(f"{month}: {top_cat} (${top_val:.2f})")

    print("----------------------------------")

# Analyze need or want category
def analyze_need_vs_want(df):
    expenses = df[df["Type"].str.lower() == "expense"]
    if "NeedOrWant" not in df.columns or expenses.empty:
        print("\nNo 'NeedOrWant' data available.")
        return

    summary = expenses.groupby("NeedOrWant")["Amount"].sum()
    total = summary.sum()
    if total == 0:
        print("\nNo spending data to analyze.")
        return

    print("\n💡 Need vs Want Spending:")
    for category, amount in summary.items():
        percentage = (amount / total) * 100
        print(f"{category}: ${amount:.2f} ({percentage:.1f}%)")
    print("----------------------------------")


def analyze_spending():
    df = load_data()
    if df.empty:
        print("\nNo transactions found for analysis.")
        return

    while True:
        print("\n==== Spending Analysis Menu ====")
        print("1. Analyze Spending by Category")
        print("2. Calculate Average Monthly Spending")
        print("3. Show Top Spending Category")
        print("4. Show Top Spending Category by Month")
        print("5. Analyze Need vs Want Spending")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == '1':
            analyze_by_category(df)
        elif choice == '2':
            average_monthly_spending(df)
        elif choice == '3':
            top_spending_category(df)
        elif choice == '4':
            top_category_by_month(df)
        elif choice == '5':
            analyze_need_vs_want(df)
        elif choice == '6':
            break
        else:
            print("Invalid choice. Try again.")
