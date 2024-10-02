# shoppinglist.py

# Empty list for the shopping list
shopping_list = []

def add_item():
    # Input for the item
    item = input("Please enter the item to add to the shopping list: ")
    # Add the item to the list
    shopping_list.append(item)
    # Print confirmation message
    print(f"{item} has been added to the shopping list.")

# For testing
if __name__ == "__main__":
    add_item()

    # Function to display the shopping list
def show_shoppinglist():
    if shopping_list:
        print("Your shopping list:")
        for item in shopping_list:
            print(f"- {item}")
    else:
        print("Your shopping list is empty.")

# For testing
if __name__ == "__main__":
    show_shoppinglist()
