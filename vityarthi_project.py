"""
Simple ATM / Money Management System

Run: python atm.py
Storage: accounts.json
"""

import json
import os
import sys
import uuid
import hashlib
from datetime import datetime

DATA_FILE = "accounts.json"
SALT = "simple_atm_salt_2024"


def now_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def hash_pin(pin):
    return hashlib.sha256((SALT + pin).encode()).hexdigest()


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"accounts": {}}
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def generate_account_number():
    return uuid.uuid4().hex[:10].upper()


def print_line():
    print("\n" + "=" * 50)


class SimpleATM:
    def __init__(self):
        self.data = load_data()
        self.current_user = None

    # Get PIN using regular input (visible)
    def get_pin(self, prompt="Enter PIN: "):
        pin = input(prompt).strip()
        return pin

    def create_account(self):
        print_line()
        print("CREATE NEW ACCOUNT")
        print_line()
        
        name = input("Enter your name: ").strip()
        if not name:
            print("❌ Name cannot be empty!")
            return

        # Get PIN with visible input
        while True:
            pin = input("Create a 4-digit PIN: ").strip()
            if not pin.isdigit() or len(pin) != 4:
                print("❌ PIN must be exactly 4 digits!")
                continue
            
            confirm = input("Confirm PIN: ").strip()
            if pin != confirm:
                print("❌ PINs don't match! Try again.")
                continue
            break

        acc_no = generate_account_number()
        self.data["accounts"][acc_no] = {
            "name": name,
            "pin": hash_pin(pin),
            "balance": 0.0,
            "created": now_time(),
            "history": []
        }
        save_data(self.data)
        
        print("\n✅ Account created successfully!")
        print(f"📝 Your Account Number: {acc_no}")
        print("⚠️  SAVE THIS NUMBER - You need it to login!")
        input("\nPress Enter to continue...")

    def login(self):
        print_line()
        print("LOGIN")
        print_line()
        
        acc_no = input("Account Number: ").strip().upper()
        if acc_no not in self.data["accounts"]:
            print("❌ Account not found!")
            input("Press Enter to continue...")
            return False

        account = self.data["accounts"][acc_no]
        pin = self.get_pin("Enter your PIN: ")
        
        if hash_pin(pin) != account["pin"]:
            print("❌ Wrong PIN!")
            input("Press Enter to continue...")
            return False

        self.current_user = acc_no
        print(f"\n✅ Welcome, {account['name']}!")
        input("Press Enter to continue...")
        return True

    def show_balance(self):
        acc = self.data["accounts"][self.current_user]
        print_line()
        print("BALANCE")
        print_line()
        print(f"Account: {self.current_user}")
        print(f"Name: {acc['name']}")
        print(f"Balance: ₹{acc['balance']:.2f}")
        input("\nPress Enter to continue...")

    def deposit(self):
        acc = self.data["accounts"][self.current_user]
        print_line()
        print("DEPOSIT MONEY")
        print_line()
        
        try:
            amount = float(input("Enter amount to deposit: ₹"))
            if amount <= 0:
                print("❌ Amount must be positive!")
                input("Press Enter to continue...")
                return
            
            acc["balance"] += amount
            acc["history"].append({
                "time": now_time(),
                "type": "Deposit",
                "amount": amount
            })
            save_data(self.data)
            
            print(f"\n✅ Deposited ₹{amount:.2f}")
            print(f"💰 New Balance: ₹{acc['balance']:.2f}")
            input("\nPress Enter to continue...")
        except ValueError:
            print("❌ Invalid amount!")
            input("Press Enter to continue...")

    def withdraw(self):
        acc = self.data["accounts"][self.current_user]
        print_line()
        print("WITHDRAW MONEY")
        print_line()
        print(f"Available Balance: ₹{acc['balance']:.2f}")
        
        try:
            amount = float(input("Enter amount to withdraw: ₹"))
            if amount <= 0:
                print("❌ Amount must be positive!")
                input("Press Enter to continue...")
                return
            
            if amount > acc["balance"]:
                print("❌ Insufficient balance!")
                input("Press Enter to continue...")
                return
            
            acc["balance"] -= amount
            acc["history"].append({
                "time": now_time(),
                "type": "Withdraw",
                "amount": -amount
            })
            save_data(self.data)
            
            print(f"\n✅ Withdrawn ₹{amount:.2f}")
            print(f"💰 New Balance: ₹{acc['balance']:.2f}")
            input("\nPress Enter to continue...")
        except ValueError:
            print("❌ Invalid amount!")
            input("Press Enter to continue...")

    def transfer(self):
        acc = self.data["accounts"][self.current_user]
        print_line()
        print("TRANSFER MONEY")
        print_line()
        print(f"Available Balance: ₹{acc['balance']:.2f}")
        
        dest_acc = input("Enter destination account number: ").strip().upper()
        
        if dest_acc == self.current_user:
            print("❌ Cannot transfer to same account!")
            input("Press Enter to continue...")
            return
        
        if dest_acc not in self.data["accounts"]:
            print("❌ Destination account not found!")
            input("Press Enter to continue...")
            return
        
        try:
            amount = float(input("Enter amount to transfer: ₹"))
            if amount <= 0:
                print("❌ Amount must be positive!")
                input("Press Enter to continue...")
                return
            
            if amount > acc["balance"]:
                print("❌ Insufficient balance!")
                input("Press Enter to continue...")
                return
            
            # Transfer
            acc["balance"] -= amount
            self.data["accounts"][dest_acc]["balance"] += amount
            
            time = now_time()
            acc["history"].append({
                "time": time,
                "type": "Transfer Out",
                "amount": -amount,
                "to": dest_acc
            })
            self.data["accounts"][dest_acc]["history"].append({
                "time": time,
                "type": "Transfer In",
                "amount": amount,
                "from": self.current_user
            })
            save_data(self.data)
            
            print(f"\n✅ Transferred ₹{amount:.2f} to {dest_acc}")
            print(f"💰 New Balance: ₹{acc['balance']:.2f}")
            input("\nPress Enter to continue...")
        except ValueError:
            print("❌ Invalid amount!")
            input("Press Enter to continue...")

    def show_history(self):
        acc = self.data["accounts"][self.current_user]
        print_line()
        print("TRANSACTION HISTORY")
        print_line()
        
        if not acc["history"]:
            print("No transactions yet.")
        else:
            history = list(reversed(acc["history"]))[:10]  # Last 10
            for trans in history:
                amt = trans["amount"]
                sign = "+" if amt > 0 else ""
                print(f"{trans['time']} | {trans['type']:15} | {sign}₹{amt:.2f}")
        
        input("\nPress Enter to continue...")

    def change_pin(self):
        acc = self.data["accounts"][self.current_user]
        print_line()
        print("CHANGE PIN")
        print_line()
        
        old_pin = self.get_pin("Enter current PIN: ")
        if hash_pin(old_pin) != acc["pin"]:
            print("❌ Wrong current PIN!")
            input("Press Enter to continue...")
            return
        
        while True:
            new_pin = input("Enter new 4-digit PIN: ").strip()
            if not new_pin.isdigit() or len(new_pin) != 4:
                print("❌ PIN must be exactly 4 digits!")
                continue
            
            confirm = input("Confirm new PIN: ").strip()
            if new_pin != confirm:
                print("❌ PINs don't match!")
                continue
            break
        
        acc["pin"] = hash_pin(new_pin)
        save_data(self.data)
        print("\n✅ PIN changed successfully!")
        input("Press Enter to continue...")

    def logout(self):
        self.current_user = None
        print("\n✅ Logged out successfully!")
        input("Press Enter to continue...")

    def main_menu(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print_line()
            print("🏦 SIMPLE ATM SYSTEM")
            print_line()
            print("1. Create Account")
            print("2. Login")
            print("3. Exit")
            print_line()
            
            choice = input("Choose option (1-3): ").strip()
            
            if choice == "1":
                self.create_account()
            elif choice == "2":
                if self.login():
                    self.user_menu()
            elif choice == "3":
                print("\n👋 Thank you for using ATM. Goodbye!")
                sys.exit(0)
            else:
                print("❌ Invalid option!")
                input("Press Enter to continue...")

    def user_menu(self):
        while self.current_user:
            os.system('cls' if os.name == 'nt' else 'clear')
            acc = self.data["accounts"][self.current_user]
            print_line()
            print(f"🏦 ACCOUNT: {self.current_user}")
            print(f"👤 {acc['name']} | 💰 Balance: ₹{acc['balance']:.2f}")
            print_line()
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Transfer Money")
            print("5. Transaction History")
            print("6. Change PIN")
            print("7. Logout")
            print_line()
            
            choice = input("Choose option (1-7): ").strip()
            
            if choice == "1":
                self.show_balance()
            elif choice == "2":
                self.deposit()
            elif choice == "3":
                self.withdraw()
            elif choice == "4":
                self.transfer()
            elif choice == "5":
                self.show_history()
            elif choice == "6":
                self.change_pin()
            elif choice == "7":
                self.logout()
            else:
                print("❌ Invalid option!")
                input("Press Enter to continue...")


if __name__ == "__main__":
    print("\n🏦 Welcome to Simple ATM System!\n")
    atm = SimpleATM()
    try:
        atm.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)