import sqlite3

def submit_data(name, email, phone):
    """
    Connects to the database and inserts the customer's information.
    
    Args:
        name (str): The customer's full name.
        email (str): The customer's email address.
        phone (str): The customer's phone number.
    """
    # 1. Connect to the database file
    # If the file doesn't exist, it will be created.
    # The 'with' statement ensures the connection is closed automatically.
    try:
        conn = sqlite3.connect('customer_data.db')
        cursor = conn.cursor()

        # 2. Define the SQL INSERT statement
        # This assumes your table is called 'customers' and has columns 
        # 'name', 'email', and 'phone'.
        sql_insert = """
        INSERT INTO customers (name, email, phone) 
        VALUES (?, ?, ?);
        """

        # 3. Execute the SQL command
        # ALWAYS use the parameterized form (the '?' placeholders) to prevent 
        # SQL Injection security vulnerabilities.
        customer_info = (name, email, phone)
        cursor.execute(sql_insert, customer_info)

        # 4. Commit (save) the changes to the database
        conn.commit()
        print("✅ Customer data saved successfully!") # For testing/logging

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")

    finally:
        # 5. Close the connection
        if 'conn' in locals() and conn:
            conn.close()

# --- Example of how you would call this function ---
# (The actual values would come from your GUI input fields)
# submit_data("Jane Doe", "jane@example.com", "555-1234")