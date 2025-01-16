import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime  # Import datetime module
from tkinter import Tk, Canvas



conn = sqlite3.connect('inventory.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS inventory
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              item_name TEXT,
              quantity INTEGER)''')
conn.commit()

# Function to update current date and time
def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def add_item():
    item_name = item_entry.get().strip().lower()
    quantity = quantity_entry.get().strip()

    if item_name and quantity:
        try:
            quantity = int(quantity)

            if quantity > 0:
                c.execute("SELECT * FROM inventory WHERE LOWER(item_name) = ?", (item_name,))
                existing_item = c.fetchone()

                if existing_item:
                    messagebox.showerror("Error", "Item already exists.")
                else:
                    c.execute("INSERT INTO inventory (item_name, quantity) VALUES (?, ?)",
                              (item_name, quantity))
                    conn.commit()
                    messagebox.showinfo("Success", "Item added successfully.")
                    item_entry.delete(0, tk.END)
                    quantity_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Quantity should be greater than 0.")
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity. Please enter a valid number.")
    else:
        messagebox.showerror("Error", "Please enter item name and quantity.")

def update_item():
    item_name = item_entry.get().strip().lower()
    quantity = quantity_entry.get().strip()

    if item_name and quantity:
        try:
            quantity = int(quantity)

            if quantity > 0:
                c.execute("SELECT * FROM inventory WHERE LOWER(item_name) = ?", (item_name,))
                existing_item = c.fetchone()

                if existing_item:
                    c.execute("UPDATE inventory SET quantity=? WHERE LOWER(item_name)=?",
                              (quantity, item_name))
                    conn.commit()
                    messagebox.showinfo("Success", "Item updated successfully.")
                    item_entry.delete(0, tk.END)
                    quantity_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", "Item does not exist.")
            else:
                messagebox.showerror("Error", "Quantity should be greater than 0.")
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity. Please enter a valid number.")
    else:
        messagebox.showerror("Error", "Please enter item name and quantity.")

def remove_item():
    item_name = item_entry.get().strip().lower()

    if item_name:
        c.execute("SELECT * FROM inventory WHERE LOWER(item_name) = ?", (item_name,))
        existing_item = c.fetchone()

        if existing_item:
            confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to remove the item?")
            if confirmation:
                c.execute("DELETE FROM inventory WHERE LOWER(item_name) = ?", (item_name,))
                conn.commit()
                messagebox.showinfo("Success", "Item removed successfully.")
                item_entry.delete(0, tk.END)
                quantity_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Item does not exist.")
    else:
        messagebox.showerror("Error", "Please enter item name.")

def view_inventory():
    c.execute("SELECT * FROM inventory")
    rows = c.fetchall()
    inventory_text.delete(1.0, tk.END)

    # Show current date and time at the top of the inventory window
    current_datetime = get_current_datetime()
    inventory_text.insert(tk.END, f"Current Date & Time: {current_datetime}\n\n")

    if rows:
        inventory_text.insert(tk.END, "Current Inventory:\n")
        for row in rows:
            inventory_text.insert(tk.END, f"ID: {row[0]}, Item Name: {row[1]}, Quantity: {row[2]}\n")
    else:
        inventory_text.insert(tk.END, "Inventory is empty.")

def search_item():
    item_name = item_entry.get().strip().lower()
    if item_name:
        c.execute("SELECT * FROM inventory WHERE LOWER(item_name) = ?", (item_name,))
        rows = c.fetchall()
        if rows:
            result = "Search Results:\n"
            for row in rows:
                result += f"ID: {row[0]}, Item Name: {row[1]}, Quantity: {row[2]}\n"
        else:
            result = "Item not found."
        messagebox.showinfo("Search Results", result)
    else:
        messagebox.showerror("Error", "Please enter item name.")

def clear_fields():
    item_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)

window = tk.Tk()
window.title("MAD Inventory System")
window.geometry("500x400")
window['background']='#f0ece2'

header_label = tk.Label(window, text="MAD Inventory", font=("Georgia", 40, "bold"), pady=20, bg="#f0ece2")
header_label.pack()

input_frame = tk.Frame(window, bg="#b7c9e2", highlightbackground="#010101", highlightthickness=3)
input_frame.pack(pady=100, padx=50)

input_frame.config(width=700)

item_label = tk.Label(input_frame, text="Item Name:", bg="#b7c9e2", font=("Verdana", 9, "bold"))
item_label.grid(row=0, column=0, padx=10, pady=5)
item_entry = tk.Entry(input_frame, width=30)
item_entry.grid(row=0, column=1, padx=10, pady=5)

quantity_label = tk.Label(input_frame, text="Quantity:", bg="#b7c9e2", font=("Verdana", 9, "bold"))
quantity_label.grid(row=1, column=0, padx=10, pady=5)
quantity_entry = tk.Entry(input_frame, width=30)
quantity_entry.grid(row=1, column=1, padx=10, pady=5)

add_button = tk.Button(input_frame, text="Add Item", width=15, command=add_item)
add_button.grid(row=2, column=0, padx=10, pady=5)

update_button = tk.Button(input_frame, text="Update Item", width=15, command=update_item)
update_button.grid(row=2, column=1, padx=10, pady=5)

search_button = tk.Button(input_frame, text="Search Item", width=15, command=search_item)
search_button.grid(row=3, column=0, padx=10, pady=5)

remove_button = tk.Button(input_frame, text="Remove Item", width=15, command=remove_item)
remove_button.grid(row=3, column=1, padx=10, pady=5)

clear_button = tk.Button(input_frame, text="Clear", width=15, command=clear_fields)
clear_button.grid(row=4, column=0, padx=10, pady=5)

inventory_frame = tk.Frame(window, highlightbackground="#b7c9e2", highlightthickness=3)
inventory_frame.pack(pady=20)

inventory_text = tk.Text(inventory_frame, height=10, width=50)
inventory_text.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar = tk.Scrollbar(inventory_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
inventory_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=inventory_text.yview)

def switch_to_inventory_view():
    input_frame.pack_forget()
    inventory_frame.pack(pady=20)
    view_inventory_button.pack_forget()
    back_button.pack(side=tk.LEFT, padx=10)
    view_inventory()

def switch_to_input_view():
    inventory_frame.pack_forget()
    input_frame.pack(pady=20)
    view_inventory_button.pack(side=tk.LEFT, padx=10)
    back_button.pack_forget()
    clear_fields()

view_inventory_button = tk.Button(window, text="View Inventory", width=15, command=switch_to_inventory_view)
view_inventory_button.pack(side=tk.LEFT, padx=10)

back_button = tk.Button(window, text="Back", width=10, command=switch_to_input_view)
back_button.pack_forget()

switch_to_input_view()

window.mainloop()

conn.close()
