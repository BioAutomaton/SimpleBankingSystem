import sqlite3
from random import randint

conn = sqlite3.connect("card.s3db")
cur = conn.cursor()
INN = "400000"

#  cur.execute("DROP TABLE IF EXISTS card;")

cur.execute("CREATE TABLE IF NOT EXISTS card("
            "id INTEGER,"
            "number TEXT,"
            "pin TEXT,"
            "balance INTEGER);")


class BankAccount:

    def __init__(self, id=None, number=None, pin=None, balance=None):

        if id:
            self.id = id
        else:
            cur.execute("SELECT count(*) FROM card")
            self.id = cur.fetchone()[0] + 1

        if number:
            self.number = number
        else:  # if there is no number given, generate one
            account_identifier = "{:09}".format(randint(0, 10 ** 9 - 1))
            luhn_algorithm = list(INN + account_identifier)

            # step 1: multiply odd digits by 2
            for i in range(15):
                digit = int(luhn_algorithm[i])
                if (i + 1) % 2 != 0:
                    luhn_algorithm[i] = str(digit * 2)

            # step 2: subtract 9 from numbers over 9
            for i in range(15):
                digit = int(luhn_algorithm[i])
                if digit > 9:
                    luhn_algorithm[i] = str(digit - 9)

            # step 3: add all numbers and generate checksum
            control_number = 0
            for digit in luhn_algorithm:
                control_number += int(digit)
            control_number %= 10
            checksum = str((10 - control_number) % 10)
            self.number = INN + account_identifier + checksum

        if pin:
            self.PIN = pin
        else:
            self.PIN = "{:04}".format(randint(0, 9999))

        if balance:
            self.balance = balance
        else:
            self.balance = 0

    def is_correct(self, card_pin):
        return True if card_pin == self.PIN else False

    def get_number(self):
        return self.number

    #  to display info to user
    def get_card_info(self):
        return f"Your card number:\n{self.number}\nYour card PIN:\n{self.PIN}"

    #  whether or not card number passes the Luhn algorithm
    @staticmethod
    def luhn_checker(number):
        luhn = list(number)
        last_digit = int(luhn[-1])
        luhn.__delitem__(-1)
        for i in range(15):
            luhn[i] = int(luhn[i])

        for i in range(15):
            if (i + 1) % 2 != 0:
                luhn[i] = luhn[i] * 2

        for i in range(15):
            if luhn[i] > 9:
                luhn[i] -= 9

        digit_sum = sum(luhn)

        return True if last_digit == (10 - (digit_sum % 10) % 10) else False

    def add_to_DB(self, connection):
        cur = connection.cursor()

        query = """INSERT INTO card(id, number, pin, balance) VALUES(?, ?, ?, ?)"""
        values = (self.id, self.number, self.PIN, int(self.balance))
        cur.execute(query, values)

        connection.commit()

    def remove_from_DB(self, connection):
        cur = connection.cursor()

        query = """DELETE FROM card WHERE number = ? AND pin = ?;"""
        values = (self.number, self.PIN)
        cur.execute(query, values)

        connection.commit()

    def rewrite_in_DB(self, connection):
        #  delete current variant from the database
        self.remove_from_DB(connection)

        #  insert new variant into the database
        self.add_to_DB(connection)

    def transfer(self, connection, destination_number):
        cur = connection.cursor()
        if destination_number != self.number:
            if BankAccount.luhn_checker(destination_number):
                query = """SELECT id, number, pin, balance FROM card WHERE number = ?"""
                values = (destination_number,)
                cur.execute(query, values)

                data = cur.fetchone()
                if data:
                    destination_account = BankAccount(data[0], data[1], data[2], data[3])
                    transfer_money = int(input("Enter how much money you want to transfer:"))
                    if self.balance >= transfer_money:
                        self.balance -= transfer_money
                        destination_account.balance += transfer_money

                        self.rewrite_in_DB(connection)
                        destination_account.rewrite_in_DB(connection)

                        print("Success!")

                    else:
                        print("Not enough money!")
                else:
                    print("Such a card does not exist.")
            else:
                print("Probably you made a mistake in the card number. Please try again!")
        else:
            print("You can't transfer money to the same account!")

    def account_menu(self):
        logged_in = True
        while logged_in:
            user_choice = input("1. Balance\n"
                                "2. Add income\n"
                                "3. Do transfer\n"
                                "4. Close account\n"
                                "5. Log out\n"
                                "0. Exit\n")
            if user_choice == "1":
                print(f"Balance: {self.balance}")

            elif user_choice == "2":
                income = int(input("Enter income: "))
                self.balance += income
                self.rewrite_in_DB(conn)

            elif user_choice == "3":
                print("Transfer")
                dest_number = input("Enter card number:")
                self.transfer(conn, dest_number)
            elif user_choice == "4":
                self.remove_from_DB(conn)
                print("The account has been closed!")
                logged_in = False
            elif user_choice == "5":
                logged_in = False
            elif user_choice == "0":
                print("\nBye!")
                cur.close()
                conn.close()
                quit()

    @staticmethod
    def read_card(card_number, card_pin):
        cur.execute("SELECT id, number, pin, balance FROM card WHERE number = ? AND pin = ?",
                    (card_number, card_pin))
        data = cur.fetchone()
        if data:
            return BankAccount(data[0], data[1], data[2], data[3])
        else:
            pass


def main_menu():
    user_choice = None
    while user_choice != "0":
        user_choice = input("1. Create an account\n"
                            "2. Log into account\n"
                            "0. Exit\n")

        if user_choice == "1":
            new_card = BankAccount()
            cur.execute("INSERT INTO card(id, number, pin, balance) VALUES(?, ?, ?, ?)",
                        (new_card.id, new_card.number, new_card.PIN, new_card.balance))
            print("Your card has been created")
            print(new_card.get_card_info())
            new_card.add_to_DB(conn)
        elif user_choice == "2":
            card_number = input("Enter your card number:")
            card_pin = input("Enter your PIN:")
            retrieved_card = BankAccount.read_card(card_number, card_pin)
            if retrieved_card:
                print("You have successfully logged in!")
                retrieved_card.account_menu()
                print("You have successfully logged out!")
            else:
                print("Wrong card number or PIN!")
        elif user_choice == "0":
            print("\nBye!")
            cur.close()
            conn.close()
            quit()


main_menu()
