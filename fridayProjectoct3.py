import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re # <-- Added for email validation

# --- Database Management Functions ---

DATABASE_NAME = 'customer_data.db'

def create_database_table():
    """Connects to the database and creates the 'customers' table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            birthday TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            contact_method TEXT
        )
    ''')

    conn.commit()
    conn.close()

def insert_customer_data(name, birthday, email, phone, address, contact_method):
    """Inserts customer data into the database."""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO customers (name, birthday, email, phone, address, contact_method)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, birthday, email, phone, address, contact_method))
        
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        if conn:
            conn.close()

# --- GUI Application Class ---

class CustomerApp:
    def __init__(self, master):
        self.master = master
        master.title("Customer Information Submission")
        master.geometry("450x400") 

        # 1. Variables to hold the form data
        self.name_var = tk.StringVar()
        self.birthday_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.address_var = tk.StringVar()
        
        # Variable for the dropdown menu
        self.contact_method_var = tk.StringVar(value="Email") # Default value
        self.contact_options = ["Email", "Phone", "Mail", "Any"]

        # 2. Create the GUI Widgets
        self.create_widgets()

    def create_widgets(self):
        # Use a Frame for better organization and padding
        main_frame = ttk.Frame(self.master, padding="10 10 10 10")
        main_frame.pack(fill='both', expand=True)

        # Labels and Entry Fields (using a grid layout for clean alignment)
        fields = [
            ("Name:", self.name_var),
            ("Birthday (YYYY-MM-DD):", self.birthday_var),
            ("Email:", self.email_var),
            ("Phone Number:", self.phone_var),
            ("Address:", self.address_var)
        ]

        for i, (label_text, var) in enumerate(fields):
            label = ttk.Label(main_frame, text=label_text)
            label.grid(row=i, column=0, sticky='w', pady=5, padx=5)
            
            entry = ttk.Entry(main_frame, textvariable=var, width=40)
            entry.grid(row=i, column=1, sticky='ew', pady=5, padx=5)

        # Preferred Contact Method (Dropdown Menu)
        contact_label = ttk.Label(main_frame, text="Preferred Contact Method:")
        contact_label.grid(row=len(fields), column=0, sticky='w', pady=5, padx=5)
        
        contact_menu = ttk.OptionMenu(
            main_frame, self.contact_method_var, 
            self.contact_method_var.get(), *self.contact_options
        )
        contact_menu.grid(row=len(fields), column=1, sticky='ew', pady=5, padx=5)
        contact_menu.config(width=37)

        # Submit Button
        submit_button = ttk.Button(
            main_frame, 
            text="Submit Information", 
            command=self.submit_data
        )
        # Place button below all fields, spanning two columns
        submit_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=20)

    def clear_form(self):
        """Clears all input fields after submission."""
        self.name_var.set("")
        self.birthday_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.address_var.set("")
        self.contact_method_var.set("Email") # Reset dropdown to default

    # --- VALIDATION HELPER METHODS ---
    def is_valid_email(self, email):
        """Simple check for a valid email format using regex."""
        # Regex pattern for basic email validation
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email)

    def is_valid_date(self, date_str):
        """Checks if the date string is in YYYY-MM-DD format."""
        # Check for correct length and presence of hyphens
        if len(date_str) != 10:
            return False
        if date_str[4] != '-' or date_str[7] != '-':
            return False
        # Check if the parts are digits
        if not (date_str[:4].isdigit() and date_str[5:7].isdigit() and date_str[8:].isdigit()):
            return False
        return True
    # --- END VALIDATION HELPER METHODS ---

    def submit_data(self):
        """Handles the submission process with validation, insertion, and form clearing."""
        # Get data from variables
        name = self.name_var.get().strip()
        birthday = self.birthday_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        address = self.address_var.get().strip()
        contact_method = self.contact_method_var.get().strip()

        # --- DATA VALIDATION BLOCK ---

        # 1. Required Field Validation (Name)
        if not name:
            messagebox.showerror("Validation Error", "Customer **Name** is a required field.")
            return

        # 2. Email Format Validation (only if email is provided)
        if email and not self.is_valid_email(email):
            messagebox.showerror("Validation Error", "Please enter a valid **Email** address (e.g., user@example.com).")
            return
            
        # 3. Date Format Validation (only if birthday is provided)
        if birthday and not self.is_valid_date(birthday):
            messagebox.showerror("Validation Error", "Please enter a valid **Birthday** in YYYY-MM-DD format.")
            return

        # --- END VALIDATION BLOCK ---

        # Insert data into database
        success = insert_customer_data(name, birthday, email, phone, address, contact_method)

        if success:
            messagebox.showinfo("Success", "Customer information submitted successfully!")
            self.clear_form() # Clear the form as required
        else:
            messagebox.showerror("Error", "Failed to save information to the database.")

# --- Main Execution Block ---

if __name__ == "__main__":
    # 1. Ensure the database and table exist
    create_database_table()
    
    # 2. Start the Tkinter application
    root = tk.Tk()
    app = CustomerApp(root)
    root.mainloop()