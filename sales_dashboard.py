import pandas as pd
import matplotlib.pyplot as plt


def show_money(amount):
    if amount == int(amount):
        return "Rs. " + str(int(amount))
    else:
        return "Rs. " + str(round(amount, 2))


def load_file(filename):
    try:
        data = pd.read_csv(filename, dtype=str)
    except FileNotFoundError:
        print("Error: File '" + filename + "' not found.")
        return None

    dates = []
    items = []
    categories = []
    quantities = []
    prices = []

    for i in range(len(data)):
        # +2 because row 1 is header and i starts from 0
        row_number = i + 2

        date = str(data.loc[i, "Date"]).strip()
        item = str(data.loc[i, "Item"]).strip()
        category = str(data.loc[i, "Category"]).strip()
        qty = str(data.loc[i, "Quantity"]).strip()
        price = str(data.loc[i, "Price"]).strip()

        if item == "" or item == "nan" or category == "" or category == "nan":
            print("Warning: Row " + str(row_number) + " skipped - Item and Category cannot be empty.")
            continue

        try:
            pd.to_datetime(date, format="%Y-%m-%d")
        except ValueError:
            print("Warning: Row " + str(row_number) + " skipped - Date must be in YYYY-MM-DD format.")
            continue

        try:
            qty = int(qty)
        except ValueError:
            print("Warning: Row " + str(row_number) + " skipped - Quantity must be a number.")
            continue

        if qty <= 0:
            print("Warning: Row " + str(row_number) + " skipped - Quantity must be greater than 0.")
            continue

        try:
            price = float(price)
        except ValueError:
            print("Warning: Row " + str(row_number) + " skipped - Price must be a number.")
            continue

        if price <= 0:
            print("Warning: Row " + str(row_number) + " skipped - Price must be greater than 0.")
            continue

        dates.append(date)
        items.append(item)
        categories.append(category)
        quantities.append(qty)
        prices.append(price)

    if len(items) == 0:
        print("Error: No valid rows found in file.")
        return None

    df = pd.DataFrame({
        "Date": dates,
        "Item": items,
        "Category": categories,
        "Quantity": quantities,
        "Price": prices
    })

    # Sales = Quantity x Price
    df["Sales"] = df["Quantity"] * df["Price"]
    return df


def category_sales(df):
    result = df.groupby("Category")["Sales"].sum()
    result = result.sort_values(ascending=False)

    for category in result.index:
        print(category + " : " + show_money(result[category]))

    print("Total sales: " + show_money(df["Sales"].sum()))

    result.plot(kind="bar")
    plt.title("Sales by Category")
    plt.xlabel("Category")
    plt.ylabel("Sales (Rs.)")
    plt.xticks(rotation=0)
    plt.show()


def top_items(df):
    qty_data = df.groupby("Item")["Quantity"].sum()
    sales_data = df.groupby("Item")["Sales"].sum()

    best_qty_item = qty_data.idxmax()
    best_qty = qty_data.max()
    if best_qty == 1:
        print("Top item by quantity: " + best_qty_item + " (1 unit)")
    else:
        print("Top item by quantity: " + best_qty_item + " (" + str(best_qty) + " units)")

    best_sales_item = sales_data.idxmax()
    best_sales = sales_data.max()
    print("Top item by revenue: " + best_sales_item + " (" + show_money(best_sales) + ")")

    sales_data.sort_values(ascending=False).plot(kind="bar")
    plt.title("Revenue by Item")
    plt.xlabel("Item")
    plt.ylabel("Revenue (Rs.)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def daily_sales(df):
    result = df.groupby("Date")["Sales"].sum()

    for day in result.index:
        print(day + " : " + show_money(result[day]))

    print("Best day: " + result.idxmax())

    result.plot(kind="line", marker="o")
    plt.title("Daily Sales")
    plt.xlabel("Date")
    plt.ylabel("Sales (Rs.)")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


filename = input("Enter CSV file name: ")
df = load_file(filename)

if df is not None:
    while True:
        print()
        print("===== Restaurant Sales Dashboard =====")
        print("1. Sales by category")
        print("2. Top items")
        print("3. Top items and daily sales")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            category_sales(df)
        elif choice == "2":
            print("Total sales: " + show_money(df["Sales"].sum()))
            top_items(df)
        elif choice == "3":
            top_items(df)
            daily_sales(df)
        elif choice == "4":
            print("Thank you!")
            break
        else:
            print("Wrong choice. Enter 1 to 4.")
