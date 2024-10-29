import csv


def validate_atm(imei, token):
    with open("atm.csv", "r") as file:
        reader = csv.DictReader(file)
        for i in reader:
            if i["imei"] == imei:
                if i["token"] == token:
                    return True


def read_db(card_num, pin, imei, token):
    if validate_atm(imei, token):
        with open("accounts.csv", "r") as file:
            reader = csv.DictReader(file)
            accounts = []
            for i in reader:
                accounts.append(i)

        for index, value in enumerate(accounts):
            if value["card number"] == card_num:
                if value["pin"] == pin:
                    return accounts, index


def write_db(accounts):
    with open("accounts.csv", "w") as file:
        writer = csv.DictWriter(file, fieldnames=["first name","last name",
                                                  "card number","pin",
                                                  "checking","savings"])
        writer.writeheader()
        writer.writerows(accounts)


def cash_check(acc_num, rout_num, amt):
    with open("global.csv", "r") as f:
        reader = list(csv.DictReader(f))

        for index, value in enumerate(reader):
            if value["account_num"] == acc_num:
                if value["routing_num"] == rout_num:
                    if float(value["balance"]) >= float(amt):
                        return reader, index


def update_global_balance(all_accounts):
    with open("global.csv", "w") as file:
        writer = csv.DictWriter(file, fieldnames=["account_num", "routing_num",
                                                  "balance"])

        writer.writeheader()
        writer.writerows(all_accounts)






