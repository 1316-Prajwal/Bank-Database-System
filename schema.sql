CREATE DATABASE IF NOT EXISTS bank_db;
USE bank_db;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Accounts Table
CREATE TABLE IF NOT EXISTS accounts (
    account_number INT PRIMARY KEY,
    user_id INT NOT NULL,
    account_type ENUM('Savings', 'Checking') DEFAULT 'Savings',
    balance DECIMAL(15, 2) DEFAULT 0.00,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Transactions Table
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_number INT NOT NULL,
    transaction_type ENUM('Deposit', 'Withdrawal', 'Transfer') NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_number) REFERENCES accounts(account_number) ON DELETE CASCADE
);

-- Seed Initial Data
INSERT INTO users (user_id, full_name, email, password_hash) 
VALUES (1, 'John Doe', 'john@example.com', 'scrypt:32768:8:1$hash_placeholder');

INSERT INTO accounts (account_number, user_id, account_type, balance) 
VALUES (1001001, 1, 'Savings', 5000.00);

INSERT INTO transactions (account_number, transaction_type, amount) 
VALUES (1001001, 'Deposit', 5000.00);