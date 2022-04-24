from random import randint

import SimpleQIWI as sq
from pyqiwip2p import QiwiP2P

from config import qiwi_token

import codecs


def random_auth_code():
    code = ""
    for i in range(24):
        r = randint(0, 10)
        code += str(r)
    return str(code)


def add_user(id):
    f = codecs.open("additional\\data\\users.txt", "r", "utf_8_sig")
    all_users = f.read()
    row = all_users.strip("*").split("*")
    for user_id in row:
        if user_id in row:
            row.remove(user_id)
    row.append(f"{id}\n")
    row = "\n".join(row)
    f = codecs.open("additional\\data\\users.txt", "w", "utf_8_sig")
    f.write(row)
    f.close()


def get_user_info(user_id):
    f = codecs.open("additional\\data\\users.txt", "r", "utf_8_sig")
    all_trans = f.read()
    row = all_trans.strip("*").split("*")
    for i in row:
        user_info = i.split('|')
        if str(user_info[0]) == str(user_id):
            f.close()
            return user_info


def quant_acc():
    f = codecs.open("additional\\data\\accounts.txt", "r", "utf_8_sig")
    all_acc = f.read()
    row = all_acc.strip("*").split("*")
    f.close()
    return len(row)


def get_all_account():
    f = codecs.open("additional\\data\\accounts.txt", "r", "utf_8_sig")
    all_acc = f.read()
    row = all_acc.strip("*").split("*")
    all_accounts = []
    for i in row:
        acc_info = i.split('|')
        all_accounts.append(acc_info)
    f.close()
    return all_accounts


def get_all_users():
    f = codecs.open("additional\\data\\users.txt", "r", "utf_8_sig")
    all_users = f.read()
    return all_users


def get_all_trans():
    f = codecs.open("additional\\data\\transactions.txt", "r", "utf_8_sig")
    all_trans = f.read()
    return all_trans


def get_account(acc_call):
    f = codecs.open("additional\\data\\accounts.txt", "r", "utf_8_sig")
    all_acc = f.read()
    row = all_acc.strip("*").split("*")
    for i in row:
        acc_info = i.split('|')
        if str(acc_info[0]) == str(acc_call):
            f.close()
            return acc_info


def add_account(callback, price, name, description):
    f = codecs.open("additional\\data\\accounts.txt", "r", "utf_8_sig")
    all_trans = f.read()
    row = all_trans.strip("*").split("*")
    row.append(f"{callback}|{price}|{name}|{description}\n")
    row = "*\n".join(row)
    f = codecs.open("additional\\data\\accounts.txt", "w", "utf_8_sig")
    f.write(row)

    f.close()


def remove_trans(id):
    f = codecs.open("additional\\data\\transaction.txt", "r", "utf_8_sig")
    all_trans = f.read()
    row = all_trans.strip("\n").split("\n")
    for i in row:
        i = i.split('|')
        user_id = i[0]
        auth = i[1]
        if str(user_id) == str(id):
            del (i)
            row = "\n".join(row)
            f = codecs.open("additional\\data\\transaction.txt", "w", "utf_8_sig")
            f.write(all_trans)
        else:
            continue
    f.close()


def remove_acc(call):
    f = codecs.open("additional\\data\\accounts.txt", "r", "utf_8_sig")
    all_acc = f.read()
    row = all_acc.strip("*").split("*")
    for i in row:
        ii = i.split('|')
        callback = ii[0]
        if str(callback) == str(call):
            row.remove(i)
            row = "*\n".join(row)
            f = codecs.open("additional\\data\\accounts.txt", "w", "utf_8_sig")
            f.write(all_acc)
        else:
            continue
    f.close()


def find_trans(id):
    f = codecs.open("additional\\data\\transaction.txt", "r", "utf_8_sig")
    all_trans = f.read()
    row = all_trans.strip("\n").split("\n")
    for i in row[::-1]:
        i = i.split('|')
        user_id = i[0]
        auth = i[1]
        if str(user_id) == str(id):
            f.close()
            return auth
    f.close()


def add_trans(id, auth):
    f = codecs.open("additional\\data\\transaction.txt", "r", "utf_8_sig")
    all_trans = f.read()
    row = all_trans.strip("\n").split("\n")
    new_trans = f"{id}|{auth}\n"
    row.append(new_trans)
    row = "\n".join(row)
    f = codecs.open("additional\\data\\transaction.txt", "w", "utf_8_sig")
    f.write(row)
    f.close()
    return


def random_login_and_password():
    f = codecs.open("additional\\data\\login.txt", "r", "utf_8_sig")
    all_log = f.read()
    row = all_log.strip("\n").split("\n")
    index = randint(0, len(row))
    return row[index]


def my_wallet():
    api = sq.QApi(token="5c2a57688b7e7c3af17c2b7e9bf65c39", phone="+79524244227")
    return api.balance


def create_trans(amount=400, lifetime=30, comment="Aккаунт", bill_id=0000000):
    p2p = QiwiP2P(auth_key=qiwi_token)
    bill = p2p.bill(amount=amount, lifetime=lifetime, comment=comment, bill_id=bill_id)
    return bill
