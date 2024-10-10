import sqlite3
import tkinter as tk
from tkinter import messagebox

# Connect to SQLite database
conn = sqlite3.connect('shopping_list.db')
c = conn.cursor()

# Create categories table
c.execute('''CREATE TABLE IF NOT EXISTS categories
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              name TEXT NOT NULL)''')

# Create groceries table with a foreign key for categories
c.execute('''CREATE TABLE IF NOT EXISTS groceries
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              name TEXT NOT NULL, 
              amount INTEGER NOT NULL, 
              price REAL NOT NULL,
              category_id INTEGER,
              FOREIGN KEY (category_id) REFERENCES categories(id))''')

conn.commit()

# Function to close the database connection
def close_connection():
    conn.close()

# Add a category
def add_category(name):
    c.execute("INSERT INTO categories (name) VALUES (?)", (name,))
    conn.commit()
    print(f"Category '{name}' has been added.")

# Show all categories
def show_categories():
    c.execute("SELECT * FROM categories")
    categories = c.fetchall()
    if categories:
        print("Categories:")
        for category in categories:
            print(f"ID: {category[0]}, Name: {category[1]}")
    else:
        print("No categories found.")

# Show items by category
def show_items_by_category(category_name):
    c.execute('''SELECT groceries.id, groceries.name, groceries.amount, groceries.price 
                 FROM groceries 
                 INNER JOIN categories ON groceries.category_id = categories.id 
                 WHERE categories.name = ?''', (category_name,))
    items = c.fetchall()
    if items:
        print(f"Items in category '{category_name}':")
        for item in items:
            print(f"ID: {item[0]}, Name: {item[1]}, Amount: {item[2]}, Price: {item[3]}")
    else:
        print(f"No items found in category '{category_name}'.")

# Create: Add a new item to the database
def add_item_to_db(name, amount, price, category_id):
    c.execute("INSERT INTO groceries (name, amount, price, category_id) VALUES (?, ?, ?, ?)", (name, amount, price, category_id))
    conn.commit()
    print(f"{name} has been added to the shopping list.")

# Read: Show all items from the database
def show_shoppinglist_from_db():
    c.execute("SELECT * FROM groceries")
    items = c.fetchall()
    if items:
        print("Your shopping list:")
        for item in items:
            print(f"ID: {item[0]}, Name: {item[1]}, Amount: {item[2]}, Price: {item[3]}")
    else:
        print("Your shopping list is empty.")

# Update: Update an item in the database
def update_item_in_db(item_id, new_name, new_amount, new_price, new_category_id):
    c.execute("UPDATE groceries SET name = ?, amount = ?, price = ?, category_id = ? WHERE id = ?", (new_name, new_amount, new_price, new_category_id, item_id))
    conn.commit()
    print(f"Item with ID {item_id} has been updated.")

# Delete: Remove an item from the database
def delete_item_from_db(item_id):
    c.execute("DELETE FROM groceries WHERE id = ?", (item_id,))
    conn.commit()
    print(f"Item with ID {item_id} has been deleted.")

# Search for an item by name
def search_item_in_db(search_name):
    c.execute("SELECT * FROM groceries WHERE name LIKE ?", ('%' + search_name + '%',))
    items = c.fetchall()
    if items:
        print(f"Search results for '{search_name}':")
        for item in items:
            print(f"ID: {item[0]}, Name: {item[1]}, Amount: {item[2]}, Price: {item[3]}")
    else:
        print(f"No items found for '{search_name}'.")

# GUI with tkinter
def add_item_gui():
    def add_item_action():
        item_name = entry_name.get()
        item_amount = entry_amount.get()
        item_price = entry_price.get()
        category_id = entry_category_id.get()
        if item_name and item_amount and item_price and category_id:
            add_item_to_db(item_name, int(item_amount), float(item_price), int(category_id))
            messagebox.showinfo("Item Added", f"Added {item_name} (Amount: {item_amount}, Price: {item_price}, Category: {category_id})")
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields.")

    # Create window for adding item
    add_item_window = tk.Toplevel(root)
    add_item_window.title("Add Item")

    tk.Label(add_item_window, text="Item Name:").grid(row=0, column=0)
    entry_name = tk.Entry(add_item_window)
    entry_name.grid(row=0, column=1)

    tk.Label(add_item_window, text="Amount:").grid(row=1, column=0)
    entry_amount = tk.Entry(add_item_window)
    entry_amount.grid(row=1, column=1)

    tk.Label(add_item_window, text="Price:").grid(row=2, column=0)
    entry_price = tk.Entry(add_item_window)
    entry_price.grid(row=2, column=1)

    tk.Label(add_item_window, text="Category ID:").grid(row=3, column=0)
    entry_category_id = tk.Entry(add_item_window)
    entry_category_id.grid(row=3, column=1)

    btn_add = tk.Button(add_item_window, text="Add Item", command=add_item_action)
    btn_add.grid(row=4, column=0, columnspan=2)

# Main window for the GUI
root = tk.Tk()
root.title("Shopping List Manager")

# Button to add a new item
btn_add_item = tk.Button(root, text="Add Item", command=add_item_gui)
btn_add_item.grid(row=0, column=0, padx=20, pady=10)

# Start the tkinter main loop
root.mainloop()

# Close database connection in main
if __name__ == "__main__":
    close_connection()
