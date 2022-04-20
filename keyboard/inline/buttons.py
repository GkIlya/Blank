from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from additional.function.database import *


def menu():
    Choice = InlineKeyboardMarkup(row_width=2)
    show = InlineKeyboardButton(text=" Смотреть ассортимент 💵", callback_data="show")
    profile = InlineKeyboardButton(text=" Профиль 💼", callback_data="profile")
    helps = InlineKeyboardButton(text=" Поддержка ☎️", callback_data="help")
    Choice.add(show)
    Choice.add(profile)
    Choice.add(helps)
    return Choice


def show_price():
    Prices = InlineKeyboardMarkup(row_width=quant_acc())
    for acc in get_all_account():
        try:
            text = acc[2]
            but = InlineKeyboardButton(text=text, callback_data=acc[0])
            Prices.add(but)
        except IndexError:
            print("База пустая")
    return Prices


def check_trans(url: str):
    qiwiMenu = InlineKeyboardMarkup(row_width=3)
    pay = InlineKeyboardButton(text="💸 Оплатить 💸", url=url)
    done = InlineKeyboardButton(text="✅ Я оплатил ✅", callback_data="done")
    remove = InlineKeyboardButton(text="❌ Отменить заказ ❌", callback_data="remove")
    qiwiMenu.add(pay)
    qiwiMenu.add(done)
    qiwiMenu.add(remove)
    return qiwiMenu