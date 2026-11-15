"""Smart Grocery Store Management System.

A menu-driven Python application using lists, dictionaries, loops,
conditions, functions, validation, and in-memory sales records.
"""

MIN_STOCK_WARNING = 5
MENU_OPTIONS = 8

products = [
    {"id": 101, "name": "Milk", "category": "Dairy", "price": 250.0, "stock": 20},
    {"id": 102, "name": "Bread", "category": "Bakery", "price": 180.0, "stock": 8},
    {"id": 103, "name": "Rice", "category": "Grains", "price": 320.0, "stock": 12},
]

sales_records = []


def find_product_by_id(product_id):
    """Return a product dictionary by ID, or None if not found."""
    for product in products:
        if product["id"] == product_id:
            return product
    return None


def display_product(product):
    """Display one product in a readable format."""
    print(
        f"ID: {product['id']} | Name: {product['name']} | "
        f"Category: {product['category']} | Price: Rs. {product['price']:.2f} | "
        f"Stock: {product['stock']}"
    )


def get_positive_int(prompt):
    """Read a positive integer with validation."""
    while True:
        try:
            value = int(input(prompt).strip())
            if value <= 0:
                print("Error: Enter a positive whole number.")
                continue
            return value
        except ValueError:
            print("Error: Enter a valid whole number.")


def get_non_negative_int(prompt):
    """Read a non-negative integer with validation."""
    while True:
        try:
            value = int(input(prompt).strip())
            if value < 0:
                print("Error: Enter zero or a positive whole number.")
                continue
            return value
        except ValueError:
            print("Error: Enter a valid whole number.")


def get_non_negative_float(prompt):
    """Read a non-negative price with validation."""
    while True:
        try:
            value = float(input(prompt).strip())
            if value < 0:
                print("Error: Price cannot be negative.")
                continue
            return value
        except ValueError:
            print("Error: Enter a valid numeric price.")


def add_new_product():
    """Collect and append a new product dictionary."""
    print("\n--- Add New Product ---")
    product_id = get_positive_int("Enter product ID: ")
    if find_product_by_id(product_id) is not None:
        print("Error: Product ID already exists. Choose a unique ID.")
        return

    name = input("Enter product name: ").strip()
    while not name:
        print("Error: Product name cannot be empty.")
        name = input("Enter product name: ").strip()

    category = input("Enter category: ").strip()
    while not category:
        print("Error: Category cannot be empty.")
        category = input("Enter category: ").strip()

    price = get_non_negative_float("Enter price: ")
    stock = get_non_negative_int("Enter available stock: ")

    product = {
        "id": product_id,
        "name": name,
        "category": category,
        "price": price,
        "stock": stock,
    }
    products.append(product)
    print("Product added successfully.")
    display_product(product)


def display_all_products():
    """Display every product in the product list."""
    print("\n--- All Products ---")
    if not products:
        print("No products available.")
        return
    for product in products:
        display_product(product)


def search_product():
    """Search for a product by ID or name."""
    print("\n--- Search Product ---")
    query = input("Enter product name or ID: ").strip()
    if not query:
        print("Error: Search value cannot be empty.")
        return

    matches = []
    for product in products:
        if str(product["id"]) == query or product["name"].lower() == query.lower():
            matches.append(product)

    if matches:
        for product in matches:
            display_product(product)
    else:
        print("Product not found.")


def update_product_stock():
    """Add stock or replace the available quantity for a product."""
    print("\n--- Update Product Stock ---")
    product_id = get_positive_int("Enter product ID: ")
    product = find_product_by_id(product_id)
    if product is None:
        print("Error: Product not found.")
        return

    print(f"Current stock: {product['stock']}")
    print("1. Add stock")
    print("2. Set stock quantity")
    choice = input("Choose update type: ").strip()

    if choice == "1":
        quantity = get_positive_int("Enter quantity to add: ")
        product["stock"] += quantity
    elif choice == "2":
        quantity = get_non_negative_int("Enter new stock quantity: ")
        product["stock"] = quantity
    else:
        print("Error: Invalid update option.")
        return

    print(f"Stock updated successfully. New stock: {product['stock']}")


def process_customer_sale():
    """Process a sale only when the product exists and stock is sufficient."""
    print("\n--- Process Customer Sale ---")
    product_id = get_positive_int("Enter product ID: ")
    product = find_product_by_id(product_id)
    if product is None:
        print("Error: Product not found.")
        return

    quantity = get_positive_int("Enter purchase quantity: ")
    if quantity > product["stock"]:
        print(
            f"Sale rejected: Only {product['stock']} unit(s) of "
            f"{product['name']} are available."
        )
        return

    total_amount = quantity * product["price"]
    product["stock"] -= quantity
    sales_records.append(
        {
            "product_id": product["id"],
            "product_name": product["name"],
            "quantity_sold": quantity,
            "total_amount": total_amount,
        }
    )

    print("Sale completed successfully.")
    print(f"Product: {product['name']}")
    print(f"Quantity sold: {quantity}")
    print(f"Total amount: Rs. {total_amount:.2f}")
    print(f"Remaining stock: {product['stock']}")


def view_sales_records():
    """Display all completed sales records."""
    print("\n--- Sales Records ---")
    if not sales_records:
        print("No sales records available.")
        return

    for index, sale in enumerate(sales_records, start=1):
        print(
            f"{index}. Product ID: {sale['product_id']} | "
            f"Product: {sale['product_name']} | "
            f"Quantity: {sale['quantity_sold']} | "
            f"Total: Rs. {sale['total_amount']:.2f}"
        )


def generate_store_report():
    """Display summary information calculated from products and sales."""
    print("\n--- Store Report ---")
    total_products = len(products)
    total_stock = sum(product["stock"] for product in products)
    total_transactions = len(sales_records)
    total_revenue = sum(sale["total_amount"] for sale in sales_records)
    low_stock_products = [
        product for product in products if product["stock"] < MIN_STOCK_WARNING
    ]

    print(f"Total number of products: {total_products}")
    print(f"Total available stock: {total_stock}")
    print(f"Total sales transactions: {total_transactions}")
    print(f"Total revenue generated: Rs. {total_revenue:.2f}")

    print(f"Products with stock below {MIN_STOCK_WARNING} units:")
    if low_stock_products:
        for product in low_stock_products:
            print(f"- {product['name']} ({product['stock']} units)")
    else:
        print("- None")

    if products:
        highest_price_product = max(products, key=lambda product: product["price"])
        lowest_price_product = min(products, key=lambda product: product["price"])
        print(
            f"Product with highest price: {highest_price_product['name']} "
            f"(Rs. {highest_price_product['price']:.2f})"
        )
        print(
            f"Product with lowest price: {lowest_price_product['name']} "
            f"(Rs. {lowest_price_product['price']:.2f})"
        )
    else:
        print("Product with highest price: None")
        print("Product with lowest price: None")


def show_menu():
    """Display the main application menu."""
    print("\n====================================")
    print("SMART GROCERY STORE SYSTEM")
    print("====================================")
    print("1. Add New Product")
    print("2. View All Products")
    print("3. Search Product")
    print("4. Update Product Stock")
    print("5. Process Customer Sale")
    print("6. View Sales Records")
    print("7. Generate Store Report")
    print("8. Exit")


def main():
    """Run the menu until the user chooses to exit."""
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_new_product()
        elif choice == "2":
            display_all_products()
        elif choice == "3":
            search_product()
        elif choice == "4":
            update_product_stock()
        elif choice == "5":
            process_customer_sale()
        elif choice == "6":
            view_sales_records()
        elif choice == "7":
            generate_store_report()
        elif choice == "8":
            print("Thank you for using the Smart Grocery Store System.")
            break
        else:
            print(f"Error: Choose a menu option from 1 to {MENU_OPTIONS}.")


if __Madiha Shabbir__ == "__main__":
    main()
