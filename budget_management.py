#Manages income, budget setting, and alerts.
import pandas as pd
def load_data():
    try:
        df = pd.read_csv("transactions.csv")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        return df
    except FileNotFoundError:
        print("No transaction file found.")
        return pd.DataFrame(columns=["Date", "Category", "Description", "Amount", "Type", "NeedOrWant"])

#Income management
def calculate_total_income(df, start_date=None, end_date=None):
    income_df = df[df["Type"].str.lower() == "income"]
    if start_date and end_date:
        income_df = income_df[(income_df["Date"] >= start_date) & (income_df["Date"] <= end_date)]

    total_income = income_df["Amount"].sum()
    print("\n💰 Total Income:", f"${total_income:.2f}")
    return total_income

#Set budget
def set_budget():
    try:
        budget_df = pd.read_csv("budgets.csv")
    except FileNotFoundError:
        budget_df = pd.DataFrame(columns=["Category", "MonthlyBudget"])

    print("\n==== Budget Setting ====")
    category = input("Enter category name (or 'Overall' for total budget): ").strip().title()
    amount = float(input(f"Enter monthly budget amount for {category}: $"))
    new_budget = {"Category": category, "MonthlyBudget": amount}

    if category in budget_df["Category"].values:
        budget_df.loc[budget_df["Category"] == category, "MonthlyBudget"] = amount
    else:
        budget_df = pd.concat([budget_df, pd.DataFrame([new_budget])], ignore_index=True)

    budget_df.to_csv("budgets.csv", index=False)
    print(f"\n✅ Budget for {category} set to ${amount:.2f}")

#Check budget alert
def check_budget_alerts():
    df = load_data()
    try:
        budget_df = pd.read_csv("budgets.csv")
    except FileNotFoundError:
        print("\nNo budgets found. Please set a budget first.")
        return

    expenses = df[df["Type"].str.lower() == "expense"]
    expenses["Category"] = expenses["Category"].str.title()
    total_spent = expenses.groupby("Category")["Amount"].sum()

    print("\n==== Budget Alerts ====")
    for _, row in budget_df.iterrows():
        cat = row["Category"]
        budget = row["MonthlyBudget"]
        spent = total_spent.get(cat, 0)

        if spent > budget:
            print(f"⚠️  {cat}: You have exceeded your budget by ${spent - budget:.2f}.")
        elif spent >= 0.9 * budget:
            print(f"⚠️  {cat}: You are close to your budget limit (${spent:.2f} of ${budget:.2f}).")
        else:
            print(f"✅  {cat}: Spending is within budget (${spent:.2f} of ${budget:.2f}).")

# Overall budget
    if "Overall" in budget_df["Category"].values:
        overall_budget = float(budget_df.loc[budget_df["Category"] == "Overall", "MonthlyBudget"])
        total_expense = expenses["Amount"].sum()

        if total_expense > overall_budget:
            print(f"\n⚠️  Overall: You have exceeded your total budget by ${total_expense - overall_budget:.2f}.")
        elif total_expense >= 0.9 * overall_budget:
            print(f"\n⚠️  Overall: You are close to your total budget (${total_expense:.2f} of ${overall_budget:.2f}).")
        else:
            print(f"\n✅  Overall: Spending is within total budget (${total_expense:.2f} of ${overall_budget:.2f}).")

#main menu
def manage_budget():
    while True:
        print("\n==== Budget Management Menu ====")
        print("1. View Total Income")
        print("2. Set Budget")
        print("3. Check Budget Alerts")
        print("4. Back to Main Menu")

        choice = input("Enter your choice: ")

        df = load_data()

        if choice == '1':
            start_date = input("Enter start date (YYYY-MM-DD) or press Enter to skip: ") or None
            end_date = input("Enter end date (YYYY-MM-DD) or press Enter to skip: ") or None
            calculate_total_income(df, start_date, end_date)
        elif choice == '2':
            set_budget()
        elif choice == '3':
            check_budget_alerts()
        elif choice == '4':
            break
        else:
            print("Invalid choice, please try again.")