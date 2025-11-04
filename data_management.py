#Manages loading, adding, editing, and deleting transactions.
import pandas as pd

def load_data():
    try:
        df = pd.read_csv("transactions.csv")
        print("Data loaded successfully.")
        return df
    except FileNotFoundError:
        print("No file found. Creating a new one.")
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Type", "Description"])
        df.to_csv("transactions.csv", index=False)
        return df

#view all data
def view_transactions():
    df = load_data()
    if df.empty:
        print("\nNo transactions found.")
    else:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.sort_values(by="Date" , ascending=False)
        df.index = range(1, len(df) + 1)
        print("\nAll Transactions (Sorted by Date):")
        print(df)


#View transactions by date range
def view_by_date_range():
    df = load_data()
    if df.empty:
        print("\nNo transactions to filter.")
        return

    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    try:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

        if filtered.empty:
            print("\nNo transactions found in this date range.")
        else:
            filtered = filtered.sort_values(by="Date", ascending=False)
            filtered.index = range(1, len(filtered) + 1)
            print(f"\nTransactions from {start_date} to {end_date}:")
            print(filtered)
    except Exception as e:
        print("Error filtering by date range:", e)

#Add a new transaction
def add_transaction():
    df = load_data()

    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category (e.g., Food, Rent, Salary): ")
    description = input("Enter description: ")
    amount = float(input("Enter amount: "))
    type_ = input("Enter type (Income/Expense): ")
    need_or_want = input("Is this a Need or Want? (Need/Want): ").capitalize()

    new_row = {
        "Date": date,
        "Category": category,
        "Description": description,
        "Amount": amount,
        "Type": type_.capitalize(),
        "NeedOrWant": need_or_want
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv("transactions.csv", index=False)
    print("✅ Transaction added successfully!")


#edit transaction
def edit_transaction():
    df = load_data()
    if df.empty:
        print("\nNo transactions to edit.")
        return

    df.index = range(1, len(df) + 1)
    print("\nAll Transactions:")
    print(df)

    try:
        index = int(input("\nEnter the transaction number to edit: ")) - 1
        if index not in df.index:
            print("Invalid transaction number.")
            return

        print("\nCurrent Transaction Details:")
        print(f"Date: {df.loc[index, 'Date']}")
        print(f"Category: {df.loc[index, 'Category']}")
        print(f"Description: {df.loc[index, 'Description']}")
        print(f"Amount: {df.loc[index, 'Amount']}")
        print(f"Type: {df.loc[index, 'Type']}")
        if 'NeedOrWant' in df.columns:
            print(f"NeedOrWant: {df.loc[index, 'NeedOrWant']}")

        column = input("\nEnter column name to edit (Date, Category, Description, Amount, Type, NeedOrWant): ").strip()
        if column not in df.columns:
            print("Invalid column name.")
            return

        new_value = input(f"Enter new value for '{column}': ")

        if column == "Amount":
            new_value = float(new_value)

        df.at[index, column] = new_value
        df.to_csv("transactions.csv", index=False)
        print("\n✅ Transaction updated successfully!")

        print("\nUpdated Transaction Details:")
        print(df.loc[index])

    except Exception as e:
        print("Error editing transaction:", e)


#Delete transaction
def delete_transaction():
    df = load_data()
    if df.empty:
        print("\nNo transactions to delete.")
        return

    df.index = range(1, len(df) + 1)
    print(df)

    try:
        index = int(input("Enter the transaction number to delete: ")) - 1
        if index not in df.index:
            print("Invalid transaction number.")
            return

        df = df.drop(index)
        df.to_csv("transactions.csv", index=False)
        print("🗑️ Transaction deleted successfully!")

    except Exception as e:
        print("Error deleting transaction:", e)
