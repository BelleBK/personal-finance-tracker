import data_management
import data_analysis
import visualization
import budget_management

def main_menu():
    print("\n==== Personal Financial Tracker ====")
    print("1. View All Transactions")
    print("2. View Transactions by Date Range")
    print("3. Add Transaction")
    print("4. Edit Transaction")
    print("5. Delete Transaction")
    print("6. Spending Analysis")
    print("7. View Charts")
    print("8. Budget Management")
    print("9. Exit")
    return input("Enter your choice: ")

def main():
    print("Welcome to Personal Financial Tracker!")

    while True:
        choice = main_menu()

        if choice == '1':
            data_management.view_transactions()
        elif choice == '2':
            data_management.view_by_date_range()
        elif choice == '3':
            data_management.add_transaction()
        elif choice == '4':
            data_management.edit_transaction()
        elif choice == '5':
            data_management.delete_transaction()
        elif choice == '6':
            data_analysis.analyze_spending()
        elif choice == '7':
            visualization.show_charts()
        elif choice == '8':
            budget_management.manage_budget()
        elif choice == '9':
            print("Thank you for using the app. Goodbye!")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()
