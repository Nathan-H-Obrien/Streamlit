import sqlite3
import random
import datetime
from hashlib import sha256

def get_current_datetime():
    h = datetime.datetime.now()
    return h

try:
    with sqlite3.connect('test.db') as conn:
        print("Opened database successfully")
        conn.execute('''
                    CREATE TABLE IF NOT EXISTS customers (
                    customer_id INT PRIMARY KEY,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    email VARCHAR(50),
                    password VARCHAR(50),
                    status VARCHAR(50),
                    subscription VARCHAR(50),
                    created_at TIMESTAMP,
                    FOREIGN KEY (subscription) REFERENCES subscriptions(subscription_id)
                    )
                ''')
        print("Customer Table created successfully")
        
        conn.execute('''
                    CREATE TABLE IF NOT EXISTS advisors (
                    advisor_id INT PRIMARY KEY,
                    first_name VARCHAR(50),
                    last_name VARCHAR(50),
                    email VARCHAR(50),
                    password VARCHAR(50),
                    status VARCHAR(50),
                    expertise VARCHAR(50),
                    created_at TIMESTAMP  
                    )
                ''')
        print("Advisor Table created successfully")
        
        conn.execute('''
                    CREATE TABLE IF NOT EXISTS subscriptions (
                    subscription_id INT PRIMARY KEY,
                    subscription_name VARCHAR(50),
                    subscription_type VARCHAR(50),
                    subscription_cost REAL,
                    created_at TIMESTAMP
                    )
                ''')
        print("Subscription Table created successfully")
        
        conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INT PRIMARY KEY,
                customer_id INT,
                transcation_type VARCHAR(50),
                transaction_date DATE,
                transaction_amount REAL,
                transaction_status VARCHAR(50),
                created_at TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                )
            ''')
        print("Transaction Table created successfully")
        
        conn.execute('''
                     CREATE TABLE IF NOT EXISTS appointments (
                     appointment_id INT PRIMARY KEY,
                     customer_id VARCHAR(50),
                     advisor_id VARCHAR(50),
                     appointment_date DATE,
                     appointment_status VARCHAR(50),
                     appointment_type VARCHAR(50),
                     zoom_link TEXT,
                     created_at TIMESTAMP,
                     FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                     FOREIGN KEY (advisor_id) REFERENCES advisors(advisor_id)
                     )
                    ''')
        print("Appointment Table created successfully")
                     

except sqlite3.Error as e:
    pass

def add_user(first_name, last_name, email, password):
    with sqlite3.connect('test.db') as conn:
        cursor = conn.execute('''
            SELECT * FROM customers WHERE email = ?
                ''', (email,))
        if cursor.fetchone():
            print("Email already associated with an account")
            pass
        else:
            conn.execute('''
            INSERT OR IGNORE INTO customers (customer_id, first_name, last_name, email, password, status, subscription, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (generate_id(), first_name, last_name, email, sha256(password.encode()).hexdigest(), 'active', 'basic'))

def add_advisor(first_name, last_name, email, password, status, expertise):
    with sqlite3.connect('test.db') as conn:
        cursor = conn.execute('''
            SELECT * FROM advisors WHERE email = ?
        ''', (email,))
        if cursor.fetchone():
            print("Email already associated with an account")
            pass
        else:
            conn.execute('''
                INSERT OR IGNORE INTO advisors (advisor_id, first_name, last_name, email, password, status, expertise, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (generate_id(), first_name, last_name, email, sha256(password.encode()).hexdigest(), status, expertise))

def add_subscription(subscription_name, subscription_type, subscription_cost):
    with sqlite3.connect('test.db') as conn:
        conn.execute('''
            INSERT OR IGNORE INTO subscriptions (subscription_id, subscription_name, subscription_type, subscription_cost, created_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (sha256(subscription_name.encode()).hexdigest(), subscription_name, subscription_type, subscription_cost))

def add_transaction(first_name, last_name,transcation_type, transaction_date, transaction_amount, transaction_status):
    with sqlite3.connect('test.db') as conn:
        cursor = conn.execute('''
            SELECT customer_id FROM customers WHERE first_name = ? AND last_name = ?
                ''', (first_name, last_name))
        customer_id = cursor.fetchone()[0]
        conn.execute('''
            INSERT INTO transactions (transaction_id, customer_id, transcation_type, transaction_date, transaction_amount, transaction_status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (sha256(str(get_current_datetime()).encode()).hexdigest(), customer_id, transcation_type, transaction_date, transaction_amount, transaction_status))

def add_appointment(customer_id, advisor_id, appointment_date, appointment_status, appointment_type, zoom_link):
    with sqlite3.connect('test.db') as conn:
        conn.execute('''
            INSERT OR IGNORE INTO appointments (appointment_id, customer_id, advisor_id, appointment_date, appointment_status, appointment_type, zoom_link, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (generate_id(), customer_id, advisor_id, appointment_date, appointment_status, appointment_type, zoom_link))

def get_user(email, password):
    with sqlite3.connect('test.db') as conn:
        cursor = conn.execute('''
            SELECT * FROM customers WHERE email = ? AND password = ?
        ''', (email, password))
        return cursor.fetchone()

def get_advisor(email, password):
    with sqlite3.connect('test.db') as conn:
        cursor = conn.execute('''
            SELECT * FROM advisors WHERE email = ? AND password = ?
        ''', (email, password))
        return cursor.fetchone()
    
def get_subscription(subscription_name):
    with sqlite3.connect('test.db') as conn:
        cursor = conn.execute('''
            SELECT * FROM subscriptions WHERE subscription_name = ?
        ''', (subscription_name,))
        return cursor.fetchone()

def get_transactions(customer_id):
    with sqlite3.connect('test.db') as conn:
        cursor = conn.execute('''
            SELECT * FROM transactions WHERE customer_id = ?
        ''', (customer_id,))
        return cursor.fetchall()
    
def get_appointments(customer_id):
    with sqlite3.connect('test.db') as conn:
        cursor = conn.execute('''
            SELECT * FROM appointments WHERE customer_id = ?
        ''', (customer_id,))
        return cursor.fetchall()

def get_advisor_appointments(advisor_id):
    with sqlite3.connect('test.db') as conn:
        cursor = conn.execute('''
            SELECT * FROM appointments WHERE advisor_id = ?
        ''', (advisor_id,))
        return cursor.fetchall()
    
def get_advisor_transactions(advisor_id):
    with sqlite3.connect('test.db') as conn:
        cursor = conn.execute('''
            SELECT * FROM transactions WHERE advisor_id = ?
        ''', (advisor_id,))
        return cursor.fetchall()
    
def get_all_advisors():
    with sqlite3.connect('test.db') as conn:
        cursor = conn.execute('''
            SELECT * FROM advisors
        ''')
        return cursor.fetchall()

def get_all_customers():
    with sqlite3.connect('test.db') as conn:
        cursor = conn.execute('''
            SELECT * FROM customers
        ''')
        return cursor.fetchall()

def get_all_subscriptions():
    with sqlite3.connect('test.db') as conn:
        cursor = conn.execute('''
            SELECT * FROM subscriptions
        ''')
        return cursor.fetchall()

def get_all_transactions():
    with sqlite3.connect('test.db') as conn:
        cursor = conn.execute('''
            SELECT * FROM transactions
        ''')
        return cursor.fetchall()

def get_all_appointments():
    with sqlite3.connect('test.db') as conn:
        cursor = conn.execute('''
            SELECT * FROM appointments
        ''')
        return cursor.fetchall()

def update_user_status(email, status):
    with sqlite3.connect('test.db') as conn:
        conn.execute('''
            UPDATE customers SET status = ? WHERE email = ?
        ''', (status, email))

def update_advisor_status(email, status):
    with sqlite3.connect('test.db') as conn:
        conn.execute('''
            UPDATE advisors SET status = ? WHERE email = ?
        ''', (status, email))

def update_subscription_cost(subscription_name, subscription_cost):
    with sqlite3.connect('test.db') as conn:
        conn.execute('''
            UPDATE subscriptions SET subscription_cost = ? WHERE subscription_name = ?
        ''', (subscription_cost, subscription_name))

def update_transaction_status(transaction_id, transaction_status):
    with sqlite3.connect('test.db') as conn:
        conn.execute('''
            UPDATE transactions SET transaction_status = ? WHERE transaction_id = ?
        ''', (transaction_status, transaction_id))

def update_appointment_status(appointment_id, appointment_status):
    with sqlite3.connect('test.db') as conn:
        conn.execute('''
            UPDATE appointments SET appointment_status = ? WHERE appointment_id = ?
        ''', (appointment_status, appointment_id))

def delete_user(email):
    with sqlite3.connect('test.db') as conn:
        conn.execute('''
            DELETE FROM customers WHERE email = ?
        ''', (email,))

def delete_advisor(email):
    with sqlite3.connect('test.db') as conn:
        conn.execute('''
            DELETE FROM advisors WHERE email = ?
        ''', (email,))

def delete_subscription(subscription_name):
    with sqlite3.connect('test.db') as conn:
        conn.execute('''
            DELETE FROM subscriptions WHERE subscription_name = ?
        ''', (subscription_name,))

def delete_transaction(transaction_id):
    with sqlite3.connect('test.db') as conn:
        conn.execute('''
            DELETE FROM transactions WHERE transaction_id = ?
        ''', (transaction_id,))

def delete_appointment(appointment_id):
    with sqlite3.connect('test.db') as conn:
        conn.execute('''
            DELETE FROM appointments WHERE appointment_id = ?
        ''', (appointment_id,))

def generate_id():
    return random.randint(100000, 999999)

add_user('John', 'Doe', 'john.doe@example', 'password1')
add_user('Jane', 'Doe', 'jane.doe@example', 'password2')
add_advisor('Jake', 'Smith', 'jake.smith@example', 'password3', 'active', 'finance')
add_advisor('Jill', 'Smith', 'jill.smith@example', 'password4', 'active', 'health')
add_subscription('basic', 'free', 00.00)
add_subscription('premium', 'paid', 20.00)
# Get the actual customer ID for 'John'



add_transaction('John', 'Doe', 'seminar', '2021-01-01', 100.0, 'success')
add_transaction('Jane', 'Doe', 'premium', '2021-02-01', 20.0, 'success')
add_transaction('John', 'Doe', 'class', '2021-03-01', 50.0, 'success')
#add_appointment(cuID, adID, '2021-01-01', 'success', 'In-person', 'N/A')
#add_appointment(cuID, adID, '2021-01-01', 'success', 'Zoom', 'https://zoom.us/j/123456789')
#add_appointment(cuID, adID, '2021-02-01', 'success', 'In-person', 'N/A')



    


