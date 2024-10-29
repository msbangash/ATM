import api
IMEI = "1"
TOKEN = "111"


def withdraw():
    card = input("Please enter your card number: ")
    pin = input("Please enter your pin number: ")
    account_db = api.read_db(card, pin, IMEI, TOKEN)
    if account_db:
        selection = input("Do you want to withdraw from\n[1].CHECKING\n[2].SAVINGS\n>>>: ")
        account_type = "checking" if selection == "1" else "savings" if selection == "2" else None
        while True:
            amount = float(input("Enter the amount: "))
            all_accounts, user_location = account_db
            available_balance = float(all_accounts[user_location][account_type])
            if amount <= available_balance:
                all_accounts[user_location][account_type] = available_balance - amount
                api.write_db(all_accounts)
                print(f"Success! Your new balance is ${available_balance - amount}")
                return
            else:
                print("Insufficient funds!")
    else:
        print("Error. Please try again")
        return


# Fix the check function: update the balance
def deposit():
    card = input("Please enter your card number: ")
    pin = input("Please enter your pin number: ")
    account_db = api.read_db(card, pin, IMEI, TOKEN)
    if account_db:
        selection = input("Do you want to deposit into\n[1].CHECKING\n[2].SAVINGS\n>>>: ")
        account_type = "checking" if selection == "1" else "savings" if selection == "2" else None

        selection_2 = input("Do you want to deposit a\n[1].CHECK\n[2].CASH\n>>>: ")
        if selection_2 == "1":
            account_num = input("Please enter the account num: ")
            routing_num = input("Please enter the routing num: ")
            check_amt = float(input("Please enter the check amount: "))
            try:
                global_accounts, index = api.cash_check(account_num, routing_num, check_amt)

                all_accounts, user_location = account_db
                user_balance = float(all_accounts[user_location][account_type])
                all_accounts[user_location][account_type] = user_balance + check_amt

                global_accounts[index]["balance"] = float(global_accounts[index]["balance"]) - check_amt

                api.write_db(all_accounts)
                api.update_global_balance(global_accounts)
                print(f"Success! Your new balance is $ {user_balance + check_amt}")
            except:
                print("Check bounced!")

        elif selection_2 == "2":
            cash_amt = float(input("Please enter the cash amount: "))
            all_accounts, user_location = account_db
            user_balance = float(all_accounts[user_location][account_type])
            all_accounts[user_location][account_type] = user_balance + cash_amt
            api.write_db(all_accounts)
            print(f"Success! Your new balance is $ {user_balance + cash_amt}")


# transfer between the checking and savings account
def transfer():
    card = input("Please enter your card number: ")
    pin = input("Please enter your pin number: ")
    account_db = api.read_db(card, pin, IMEI, TOKEN)

    if account_db:
        all_accounts, user_location = account_db

        selection = input("Where do you want to transfer your money into\n[1].CHECKING\n[2].SAVINGS\n>>>: ")
        source = "checking" if selection == "1" else "savings" if selection == "2" else None
        destination = "savings" if selection == "1" else "checking" if selection == "2" else None

        source_balance = float(all_accounts[user_location][source])
        destination_balance = float(all_accounts[user_location][destination])
        print(source_balance)

        transfer_amt = float(input("Please enter the amount you want to transfer: "))
        if transfer_amt <= source_balance:
            all_accounts[user_location][source] = source_balance - transfer_amt
            all_accounts[user_location][destination] = destination_balance + transfer_amt
            api.write_db(all_accounts)
            print(f"Transfer success! Your new balance is ${destination_balance + transfer_amt}")
        else:
            print("Insufficient funds")


def check_balance():
    card = input("Please enter your card number: ")
    pin = input("Please enter your pin number: ")
    account_db = api.read_db(card, pin, IMEI, TOKEN)

    if account_db:
        all_accounts, user_location = account_db
        print(f"Checking account balance ${all_accounts[user_location]["checking"]}")
        print(f"Savings account balance ${all_accounts[user_location]["savings"]}")


def main():
    while True:
        print("Welcome to the ATM interface! Please select from the following four options: ")
        selection = input("[1].WITHDRAW\n[2].DEPOSIT\n[3].TRANSFER\n[4].CHECK_BALANCE\n[5].QUIT\n>>>: ")
        if selection == "1":
            withdraw()
        elif selection == "2":
            deposit()
        elif selection == "3":
            transfer()
        elif selection == "4":
            check_balance()
        elif selection == "5":
            quit()


main()