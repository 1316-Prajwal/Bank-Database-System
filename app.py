from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'bank_secret_key'

# MySQL Configuration - MUST MATCH YOUR MYSQL WORKBENCH CREDENTIALS
db_config = {
    'host': 'localhost',
    'user': 'root',       # Your MySQL username
    'password': '',        # <-- PUT YOUR MYSQL WORKBENCH PASSWORD HERE
    'database': 'bank_db'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def dashboard():
    account_num = 1001001  # Demo Account Number created in SQL
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch User & Account Details
    cursor.execute("""
        SELECT u.full_name, a.account_number, a.account_type, a.balance 
        FROM users u 
        JOIN accounts a ON u.user_id = a.user_id 
        WHERE a.account_number = %s
    """, (account_num,))
    account = cursor.fetchone()

    # Fetch Recent Transactions
    cursor.execute("""
        SELECT transaction_type, amount, transaction_date 
        FROM transactions 
        WHERE account_number = %s 
        ORDER BY transaction_date DESC LIMIT 5
    """, (account_num,))
    transactions = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('dashboard.html', account=account, transactions=transactions)

@app.route('/transaction', methods=['POST'])
def process_transaction():
    account_num = int(request.form['account_number'])
    txn_type = request.form['type']
    amount = float(request.form['amount'])

    if amount <= 0:
        flash("Amount must be greater than zero.", "danger")
        return redirect(url_for('dashboard'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT balance FROM accounts WHERE account_number = %s", (account_num,))
    current_balance = cursor.fetchone()['balance']

    if txn_type == 'Withdrawal' and current_balance < amount:
        flash("Insufficient funds!", "danger")
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))

    # Calculate new balance
    if txn_type == 'Deposit':
        new_balance = current_balance + amount
    else:
        new_balance = current_balance - amount

    # Update database
    cursor.execute("UPDATE accounts SET balance = %s WHERE account_number = %s", (new_balance, account_num))

    # Log transaction
    cursor.execute("INSERT INTO transactions (account_number, transaction_type, amount) VALUES (%s, %s, %s)",
                   (account_num, txn_type, amount))

    conn.commit()
    cursor.close()
    conn.close()

    flash(f"Successfully processed {txn_type} of ${amount:.2f}", "success")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)