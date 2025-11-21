# Vityarthi-Project
i have made a project on ATM using python and its libraries
A beginner-friendly, secure, and lightweight console-based ATM system built using Python.
Supports account creation, secure PIN login, deposits, withdrawals, fund transfers, transaction history, and PIN updates — all stored safely in a local JSON database.

📌 Features

🔐 Account & Security
Create new accounts with:
User name
Auto-generated 10-character account number
Secure 4-digit PIN (SHA-256 + salt)
Login system with PIN verification
JSON-based data persistence

💳 Banking Operations
Check account balance
Deposit money
Withdraw money
Transfer money to another account
View last 10 transactions
Change PIN
Logout safely

🧾 Transaction History
Each transaction stores:
Timestamp
Type (Deposit / Withdraw / Transfer)
Amount
Sender / Receiver account (for transfers)

🔒 Security Mechanisms
PINs stored as SHA-256 salted hashes
Prevents:
Negative or invalid deposits
Over-withdrawal
Self-transfer
Wrong PIN login
Each session is user-isolated
