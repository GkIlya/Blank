from aiogram.dispatcher import FSMContext

from filters.fil import Admin
from keyboard.inline.buttons import *
from loader import dp
from aiogram import types
from aiogram.types import ParseMode


##########################################################################


@dp.message_handler(Admin(), commands=["allacc"])
async def get_accs(message: types.Message, state: FSMContext):
    all_accounts = get_all_account()
    msg = """"""
    for acc in all_accounts:
        msg += f"call: {acc[0]}\nname: \"{acc[2]}\"\nprice: {acc[1]}руб\n\n"
    await message.answer(msg)


@dp.message_handler(Admin(), commands=["alluser"])
async def get_userss(message: types.Message):
    all_users = get_all_users()
    await message.answer(all_users)


@dp.message_handler(Admin(), commands=["alltrans"])
async def get_transs(message: types.Message):
    all_trans = get_all_trans()
    await message.answer(all_trans)

#########################################################################


@dp.message_handler(Admin(), commands=["add"])
async def add_accs(message: types.Message, state: FSMContext):
    await message.answer("Отправь в формате call:price:name:description")
    await state.set_state("get_")


@dp.message_handler(Admin(), state="get_")
async def get_account_info(message: types.Message, state: FSMContext):
    a = message.text.split(":")
    add_account(a[0], a[1], a[2], a[3])
    await message.answer(f"Аккаунт добавлен:\n\ncallback: {a[0]}\nprice: {a[1]}\nname: {a[2]}\ndescription: {a[3]}")
    await state.finish()

###########################################################################


@dp.message_handler(Admin(), commands=["del"])
async def del_accs(message: types.Message, state: FSMContext):
    await message.answer("Отправь в формате call:price:name:description")
    await state.set_state("del_")


@dp.message_handler(Admin(), state="del_")
async def del_account_info(message: types.Message, state: FSMContext):
    remove_acc(message.text)
    await message.answer(f"Аккаунт удален")
    await state.finish()

###########################################################################


@dp.message_handler(Admin(), commands=["wallet"])
async def start(message: types.Message):
    await message.answer(f"Баланс счета\nRUB: {my_wallet()[0]}\nUSD: {my_wallet()[1]}\nEUR: {my_wallet()[2]}", parse_mode=types.ParseMode.HTML)

###########################################################################


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    add_user(message.from_user.id)
    await message.answer("Бот запущен")
    await message.answer(text="Привествую, мой маленький дота-рэпер👋\nЗдесь ты сможешь купить или продать аккаунты дота\nпо горяим ценам🔥\nЧтобы купить аккаунт просто нажми на кнопку\nи выбери понравишвийся\nДля продажи напиши админу - @satamem\n (он занесет аккаунт в базу в базу)\n\nЕсли возникут вопросы пиши, не стесняйся",
                         reply_markup=menu(), parse_mode=ParseMode.HTML)


###########################################################################

@dp.callback_query_handler(text="profile")
async def profile(call: types.CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.answer(f"Имя: {call.from_user.first_name}\nID: {call.from_user.id}\nПокупок совершил: 0\nСумма покупок: 0 руб")


@dp.callback_query_handler(text="help")
async def help(call: types.CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.answer("Контакт службы поддержки\nПо всем вопросам пишите:\n@satamem")


###########################################################################


@dp.callback_query_handler(text="back")
@dp.callback_query_handler(text="show")
async def show(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.answer(cache_time=5)
    await call.message.answer("Вот все аккаунты представлены на выбор\n\n✅ - выбор редакции или аккаунт с наилучшей\n ценой и характеристиками\n\n🔥 - топ аккаунты, высокие LVL, много MMR\nВыгодная цена)",
                              reply_markup=show_price())
    await state.set_state("get_fcall")


@dp.callback_query_handler(state="get_fcall")
async def get_butt(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    acc_info = get_account(str(call.data))
    price = acc_info[1]
    name = acc_info[2]
    description = acc_info[3]
    await call.message.answer(f"Цена: {price}\nНазвание: {name}\nОписание: {description}", reply_markup=approve(acc_info[0]))
    await state.set_state("get_call")


@dp.callback_query_handler(state="get_call")
async def get_butt(call: types.CallbackQuery, state: FSMContext):
    acc_info = get_account(str(call.data))
    price = acc_info[1]
    name = acc_info[2]
    bill_id = random_auth_code()
    bill = create_trans(amount=price, lifetime=30, comment=name, bill_id=bill_id)
    add_trans(call.message.from_user.id, bill_id)
    await call.message.answer(
        "Отличный выбор\nДля получения аккаута тебе нужно оплатить\nСчет в течении 30 минут,\n иначе он станет не действительным",
        reply_markup=check_trans(bill.pay_url))
    await state.finish()

################################################################################


# Проверка оплаты
@dp.callback_query_handler(text="done")
async def check_for_trans(call: types.CallbackQuery, state: FSMContext):
    number_trans = find_trans(call.message.from_user.id)
    print(number_trans)
    p2p = QiwiP2P(auth_key=qiwi_token)
    status = str(p2p.check(bill_id=number_trans).status)
    if status == "PAID":
        log = random_login_and_password()
        log = log.split(":")
        await call.message.answer(f"Супер, заказ оплачен✅\nЛогин: {log[0]}\nПароль: {log[1]}")
    elif status == "REJECTED":
        await call.message.answer("❌Заказ был отменен❌")
        remove_trans(call.message.from_user.id)
        await state.set_state("get_call")
    else:
        await call.message.answer("⛔️ЗАКАЗ НЕ ОПЛАЧЕН⛔️")


@dp.callback_query_handler(text="remove")
async def check_for_trans(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer("❌Заказ был отменён❌")
    remove_trans(call.message.from_user.id)
