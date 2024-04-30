import mysql.connector

# create database in the first time (if not exists)
db = mysql.connector.connect(host="localhost", user="root", password="root@123456#")
cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS bank")

# connect with database
db = mysql.connector.connect(host="localhost", user="root", password="root@123456#", database="bank")
cursor = db.cursor()
print("Database Connected")


# # Show databases
# cursor.execute("SHOW DATABASES")
# for x in cursor:
#   print(x)

# # Show tables
# cursor.execute("SHOW TABLES")
# for x in cursor:
#   print(x)

# # delete table
# cursor.execute("DROP TABLE bank_account")

# # print bank acoount table
# cursor.execute("SELECT * FROM bank_account")
# myresult = cursor.fetchall()
# for x in myresult:
#     print(x)

# Creating bank account table in the first time (if not exists)
cursor.execute("""
CREATE TABLE IF NOT EXISTS bank_account ( 
    account_number INT PRIMARY KEY,
    balance DECIMAL(10, 2) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    date_of_opening DATE NOT NULL,
    loan_amount DECIMAL(10, 2),
    salary DECIMAL(10, 2),
    credit_score INT,
    loan_term INT,
    loan_status VARCHAR(20) DEFAULT 'Not Applied')
""")

class BankAccount:
    def __init__(self, account_number, balance, customer_name):
        self.account_number = account_number
        self.balance = balance
        self.customer_name = customer_name
        sql = "SELECT * FROM bank_account WHERE account_number = %s"
        cursor.execute(sql, (account_number,))
        account = cursor.fetchone()
        if not account:
            sql = """
            INSERT INTO bank_account (account_number, date_of_opening, balance, customer_name, loan_status) 
            VALUES (%s, NOW(), %s, %s, %s)
            """
            values = (account_number, balance, customer_name, "Not Applied")
            cursor.execute(sql, values)
            db.commit()
            print("Account created successfully.")
        elif account[0]==account_number and account[1] == balance and account[2] == customer_name:
            print(f"Account with number {account_number} and name {customer_name} is already exit.")
        else:
            print("There is another account with the same number, please choose another one.")    
    
    def deposit(self, amount):
        self.balance += amount
        query = "UPDATE bank_account SET balance = %s WHERE account_number = %s"
        values = (self.balance, self.account_number)
        cursor.execute(query, values)
        db.commit()

    def withdrawal(self, amount):
        if amount > self.balance:
            print("Insufficient balance. Please check your account.")
        else:
            self.balance -= amount
            query = "UPDATE bank_account SET balance = %s WHERE account_number = %s"
            values = (self.balance, self.account_number)
            cursor.execute(query, values)
            db.commit()

    def show_customer_details(self):
        sql = "SELECT * FROM bank_account WHERE account_number = %s"
        cursor.execute(sql, (self.account_number,))
        account_data = cursor.fetchone()
        print("Name:", account_data[2])
        print("Account Number:", account_data[0])
        print("Date of Opening:", account_data[3])
        print(f"Balance: ${account_data[1]}")
        print("Loan Status:", account_data[8])
        if account_data[8] == "Approved":
            print(f"Loan Amount: ${account_data[4]}")
            
    def apply_for_loan(self, loan_amount, salary, credit_score, loan_term):
        if salary / loan_amount < 0.5 or credit_score < 600:
            print(f"Loan application was rejected {loan_amount} for the customer {self.customer_name}.")
        else:
            sql = """
            UPDATE bank_account 
            SET loan_amount = %s, salary = %s, credit_score = %s, loan_term = %s, loan_status = %s 
            WHERE account_number = %s
            """
            values = (loan_amount, salary, credit_score, loan_term, "Approved", self.account_number)
            cursor.execute(sql, values)
            db.commit()
            print(f"Loan application has been approved {loan_amount} for the customer {self.customer_name}.")

    def close_connection(self):
        cursor.close()
        db.close()

# Test
account1 = BankAccount(1, 500.00, "sara")
account1.deposit(100.00)
account1.withdrawal(70.00)
account1.show_customer_details()

# Applying for a loan
account1.apply_for_loan(500, 400, 650, 1)
account1.show_customer_details()

account1.close_connection()