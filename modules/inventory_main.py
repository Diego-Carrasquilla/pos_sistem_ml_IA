# Importaciones estándar
import os

# Importaciones locales
from inventory.add_product import add_product
from modules.inventory.list_products import list_products
from inventory.update_stock import update_stock 
from inventory.register_entry import register_entry

def show_menu():
    print("\n==== INVENTORY MENU ====")
    print("1. Add new product")
    print("2. List all products")
    print("3. Register stock entry")
    print("0. Exit")

def main():
    while True:
        show_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Product name: ")
            description = input("Description: ")
            price = float(input("Sale price: "))
            add_product(name, description, price)

        elif choice == "2":
            list_products()

        elif choice == "3":
            product_id = int(input("Product ID: "))
            quantity = int(input("Quantity to add: "))
            register_entry(product_id, quantity)

        elif choice == "0":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid option.")

if __name__ == "__main__":
    main()
