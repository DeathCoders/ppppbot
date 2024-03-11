from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import sqlite3
from config import TOKEN, bot_name
from keyboard import *
import asyncio
import datetime

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

db = sqlite3.connect('database.db')
sql = db.cursor()

#Создание базы данных

sql.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INT,
            psevdonym TEXT,
            level TEXT,
            balance FLOAT ,
            count_refs INT,
            unactive_ref INT,
            is_admin INT,
            is_support INT,
            last_withdrawal_date TEXT ,
            deposit_date TEXT,
            deposit FLOAT,
            id_refferer TEXT
            )''')
db.commit()


# ===============================================================#

#Класы для ФМС ПРОКСИ СТЕЙТ


class FSMpsevdonim(StatesGroup):
    psevdonim = State()


class WithdrawalState(StatesGroup):
    amount = State()
    withdrawal_method = State()

class GivebalanceState(StatesGroup):
    user_id = State()
    sum = State()

class TakebalanceState(StatesGroup):
    user_id = State()
    sum = State()

class ChangebalanceState(StatesGroup):
    user_id = State()
    sum = State()

class MakeadminState(StatesGroup):
    user_id = State()

class TakeadminState(StatesGroup):
    user_id = State()

# ===============================================================#
    
#Функция проверки на подпись

async def check_subscription(user_id: int, channel_id: str) -> bool:
    try:
        chat_member = await bot.get_chat_member(channel_id, user_id)
        if chat_member["status"] != "left":
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking subscription: {e}")
        return True

# ===============================================================#
    


@dp.message_handler(commands=['start'], state=None)
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    #Отримання Рефферер айді
    try:
        global referer_id
        referer_id = str(message.get_args())
        if (referer_id == user_id):
            referer_id = ''
        else:
            referer_id = str(message.text[7:])
        print(referer_id)
    except:
        await message.answer("Реферер уже не активен")
    # ===============================================================#
    channel_id = '@dispac09' # Канал для перевірки ######################################################################################

    #Перевірка на подпись і належність базі данних
    sql.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
    if sql.fetchone() is None and await check_subscription(user_id, channel_id) == False:
        await message.reply("Unicorn Team приветствует! Прежде чем продолжить, подпишитесь на наш открытый канал:",
                            reply_markup=inlbtn)
        await message.reply("Если подписался, жми на кнопку!", reply_markup=btn)

    sql.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
    if sql.fetchone() != None and await check_subscription(user_id, channel_id) == False:
        await message.reply("Чтобы продолжить, подпешись на наш канал:", reply_markup=inlbtn)
        await message.reply("Если подписался, жми на кнопку!", reply_markup=btn)

    sql.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
    if sql.fetchone() is None and await check_subscription(user_id, channel_id) == True:
        await FSMpsevdonim.psevdonim.set()
        await message.reply("Введите Ваш псевдоним инвестора")
        sql.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
        if sql.fetchone() is None:
            @dp.message_handler(state=FSMpsevdonim.psevdonim)
            async def load_psevdonim(message: types.Message, state: FSMContext):
                async with state.proxy() as data:
                    data['psevdonim'] = message.text
                async with state.proxy() as data:
                    sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)",
                                (message.from_user.id, data['psevdonim'], "mini_horse", 0, 0, 0, 0, 0, 0, 0, 0,referer_id))
                    db.commit()
                    await state.finish()
                    await message.reply("Ваш псевдоним добавлен, вы в меню", reply_markup=menu_btn)
        for count in sql.execute(f"SELECT unactive_ref FROM users WHERE user_id = '{referer_id}'"):
            print(count[0])
            sql.execute(f"UPDATE users SET unactive_ref = ? WHERE user_id = ?", (int(count[0]) + 1, referer_id))
            db.commit()

    sql.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
    if sql.fetchone() != None and await check_subscription(user_id, channel_id) == True:
        await message.reply("Вы в меню", reply_markup=menu_btn)
        user_id = message.from_user.id

    # ===============================================================#


#Кнопка перевірки на підписку
@dp.message_handler(lambda message: message.text == 'Подписался')
async def Subscribe_checking(message: types.Message):
    user_id = message.from_user.id
    channel_id = '@dispac09'

    sql.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
    if sql.fetchone() is None:
        if await check_subscription(user_id, channel_id) == True:
            await FSMpsevdonim.psevdonim.set()
            sql.execute(f"SELECT * FROM users WHERE user_id = '{user_id}'")
            if sql.fetchone() is None:
                await message.reply("Введите Ваш псевдоним инвестора")

                @dp.message_handler(state=FSMpsevdonim.psevdonim)
                async def load_psevdonim(message: types.Message, state: FSMContext):
                    async with state.proxy() as data:
                        data['psevdonim'] = message.text
                    async with state.proxy() as data:
                        sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                    (message.from_user.id, data['psevdonim'], "mini_horse", 0, 0, 0, 0, 0, 0, 0, 0,referer_id))
                        db.commit()
                        await state.finish()
                        await message.reply("Ваш псевдоним успешно добавлен, вы в меню", reply_markup=menu_btn)
            for count in sql.execute(f"SELECT unactive_ref FROM users WHERE user_id = '{referer_id}'"):
                sql.execute(f"UPDATE users SET unactive_ref = ? WHERE user_id = ?", (int(count[0]) + 1, referer_id))
                db.commit()
        else:
            await message.reply("Вы не подписаны на канал")
    else:
        await message.reply("Я знаю, что вы подписаны!", reply_markup=menu_btn)

# ===============================================================#


#Другорядні кнопки
        
@dp.message_handler(lambda message: message.text == 'Служба поддержки')
async def SL(message: types.Message):
    await message.answer("Чат с админом: @sbu_uat", reply_markup= menu_btn)


@dp.message_handler(lambda message: message.text == 'Открытый канал')
async def OC(message: types.Message):
    await message.answer("Cсылка на канал: https://t.me/+5pdycvl8iWg5NDUy", reply_markup= menu_btn)

# ===============================================================#

@dp.message_handler(lambda message: message.text == 'Личный кабинет')
async def LK(message: types.Message):
    user_id = message.from_user.id
    for i in sql.execute(f"SELECT * FROM users WHERE user_id = {user_id}"):
        global column
        column = i
    await message.answer(
        str(f"🏠Кабинет инвестора {column[1]}\nID: {column[0]}\n🦄Добро пожаловать домой, {column[1]}!\nВаш уровень: {column[2]}\n🧞 Босс, здесь Вы можете контролировать свой рабочий процесс:\n Проверить баланс\n Проверить и повысить свой уровень\n Проверить и расширить армию Ваших Единорогов"),
        reply_markup=LK_btn)

#Для ЛК
        
@dp.message_handler(lambda message: message.text == 'Назад')
async def SL(message: types.Message):
    await message.answer("Вы в главном меню",reply_markup=menu_btn)


@dp.message_handler(lambda message: message.text == 'Уровни')
async def levels(message: types.Message):
    user_id = message.from_user.id
    for i in sql.execute(f"SELECT * FROM users WHERE user_id = {user_id}"):
        global column
        column = i
    await message.answer(
        f"🦄Ваш текущий уровень: {column[2]}\nПроцент с депозита армии: #Тут щось має бути\nПроцент с маржи армии: #Тут щось має бути\nДневная маржа: #Тут щось має бути\nХолд депозита: #Тут щось має бути\nКол-во торгуемых активов: #Тут щось має бути",
        reply_markup=level_btn)


@dp.message_handler(lambda message: message.text == 'Назад к личному кабинету')
async def BTM(message: types.Message):
    user_id = message.from_user.id
    for i in sql.execute(f"SELECT * FROM users WHERE user_id = {user_id}"):
        global column
        column = i
    await message.answer(str(f"🏠Кабинет инвестора {column[1]}\nID: {column[0]}\n🦄Добро пожаловать домой, {column[1]}!\nВаш уровень: {column[2]}\n🧞 Босс, здесь Вы можете контролировать свой рабочий процесс:\n Проверить баланс\n Проверить и повысить свой уровень\n Проверить и расширить армию Ваших Единорогов"),
        reply_markup=LK_btn)


@dp.message_handler(lambda message: message.text == 'Повысить уровень')
async def up_level(message: types.Message):
    await message.answer("Выберете уровень", reply_markup=btn_levelUP)


@dp.message_handler(lambda message: message.text == 'Назад к уровням')
async def back_up_level(message: types.Message):
    await message.answer("Выберете уровень", reply_markup=btn_levelUP)

async def notify_admins_and_supports(user_id, user_name, level):
    admins = sql.execute("SELECT user_id FROM users WHERE is_admin = 1").fetchall()
    supports = sql.execute("SELECT user_id FROM users WHERE is_support = 1").fetchall()
    recipient_ids = [admin[0] for admin in admins] + [support[0] for support in supports]

    message_text = f"Запрос на уровень отправлен от:\n@{user_name}\n{user_id}\nУровень {level}"

    for recipient_id in recipient_ids:
        await bot.send_message(chat_id=recipient_id, text=message_text)

# ===============================================================#
        
#КНОПКИ ДЛЯ РІВНІВ, + ПЕРЕСИЛАННЯ САПООРТАМ

@dp.message_handler(lambda message: message.text == 'Pony')
async def level_pony(message: types.Message):
    await message.answer(
        "🦄Уровень Pony\nДепозит: от 50 до 500$\nПроцент с депозита армии: 1.2% - до 3х рефералов\n1.5% - от 3х рефералов\nПроцент с маржи армии: недоступно\nДневная маржа: 1,2% от депозита\nХолд депозита: 40 дней\nКол-во торгуемых активов: 2",
        reply_markup=btn_pony_dep)

@dp.message_handler(lambda message: message.text == 'Запросить уровень Pony')
async def level_MU(message: types.Message):
    await notify_admins_and_supports(message.from_user.id, message.from_user.username, "Pony")
    await message.answer("Запрос отправлен, вы в меню", reply_markup=LK_btn)

@dp.message_handler(lambda message: message.text == 'Horse')
async def level_horse(message: types.Message):
    await message.answer(
        "🦄Уровень Horse\nДепозит: от 501 до 1500$\nПроцент с депозита армии: 1.5% - до 3х рефералов\n1.7% - от 3х рефералов\nПроцент с маржи армии: недоступно\nДневная маржа: 1,4% от депозита\nХолд депозита: 30 дней\nКол-во торгуемых активов: 3",
        reply_markup=btn_horse_dep)

@dp.message_handler(lambda message: message.text == 'Запросить уровень Horse')
async def level_MU(message: types.Message):
    await notify_admins_and_supports(message.from_user.id, message.from_user.username, "Horse")
    await message.answer("Запрос отправлен, вы в меню", reply_markup=LK_btn)

@dp.message_handler(lambda message: message.text == 'Unicorn')
async def level_unicorn(message: types.Message):
    await message.answer(
        "🦄Уровень Unicorn\nДепозит: от 1501 до 5000$\nПроцент с депозита армии: 1.7% - до 3х рефералов\n2% - от 3х рефералов\nПроцент с маржи армии: 5%\nДневная маржа: 1,8% от депозита\nХолд депозита: 25 дней\nКол-во торгуемых активов: 6",
        reply_markup=btn_unicorn_dep)

@dp.message_handler(lambda message: message.text == 'Запросить уровень Unicorn')
async def level_MU(message: types.Message):
    await notify_admins_and_supports(message.from_user.id, message.from_user.username, "Unicorn")
    await message.answer("Запрос отправлен, вы в меню", reply_markup=LK_btn)


@dp.message_handler(lambda message: message.text == 'Magic Unicorn')
async def level_MU(message: types.Message):
    await message.answer(
        "🦄Уровень Magic Unicorn\nДепозит: от 5500$\nПроцент с депозита армии: 2.5% - до 3х рефералов\n4% - от 3х рефералов\nПроцент с маржи армии: 11%\nДневная маржа: 2,1% от депозита\nХолд депозита: 20 дней\nКол-во торгуемых активов: 14",
        reply_markup=btn_MU_dep)

@dp.message_handler(lambda message: message.text == 'Запросить уровень Magic Unicorn')
async def level_MU(message: types.Message):
    await notify_admins_and_supports(message.from_user.id, message.from_user.username, "Magic Unicorn")
    await message.answer("Запрос отправлен, вы в меню", reply_markup=LK_btn)

# ===============================================================#
    


@dp.message_handler(lambda message: message.text == 'Армия рефералов')
async def take_level_MU(message: types.Message):
    for i in sql.execute(f"SELECT count_refs, unactive_ref FROM users WHERE user_id = {message.from_user.id}"):
        global count
        count = i
    ref_link = f"https://t.me/{bot_name}?start={message.from_user.id}"
    await message.answer(f"🧞Ваша армия состоит из {count[0]} рефералов!\nУ вас есть неактивные рефералы {count[1]}, чтобы активировать они должни сделать депозит.\nТекущий процент с депозита рефералов: 0\n🦄Время расширить армию, Босс!\n Твоя реф ссылка: {ref_link}", reply_markup = LK_btn)


#Функція для оновлення балансу

async def update_balance_daily():
    users = sql.execute("SELECT user_id, balance, level FROM users").fetchall()
    for user in users:
        user_id = user[0]
        balance = user[1]
        level = user[2]
        print(f"{level} - lvl")
        if level == "Pony":
            interest_rate = 0.0012
        elif level == "Horse":
            interest_rate = 0.0014
        elif level == "Unicorn":
            interest_rate = 0.0018
        elif level == "Magic Unicorn":
            interest_rate = 0.0021
        else:
            interest_rate = 0.0
        daily_interest = balance * interest_rate
        active_referrals_count = sql.execute(f"SELECT count_refs FROM users WHERE user_id = {user_id}").fetchone()[0]
        new_balance = 0.0030 * active_referrals_count + balance + daily_interest
        print(f"0.0030 * {active_referrals_count} + {balance} + {daily_interest}")
        print(new_balance)
        #new_balance = balance + daily_interest + referral_bonus
        sql.execute(f"UPDATE users SET balance = {new_balance} WHERE user_id = {user_id}")
        db.commit()
        await set_user_level(user_id, new_balance)

# ===============================================================#

#Кнопка баліка

@dp.message_handler(lambda message: message.text == 'Баланс')
async def take_level_MU(message: types.Message):
    for i in sql.execute(f"SELECT * FROM users WHERE user_id = {message.from_user.id}"):
        balance = i[0]
        balance_message = (f"Баланс: {i[3]}\nДепозит: {i[10]}\nЗаработал: {int(i[3]) - int(i[10])}\n\n"
            "🦄 Повысьте уровень и расширьте армию для большей маржи"
        )
        await message.answer(balance_message, reply_markup=LK_btn_Balance, parse_mode="Markdown")

#===============================================================#
        
@dp.message_handler(lambda message: message.text == 'Назад в кабинет')
async def BTM(message: types.Message):
    user_id = message.from_user.id
    for i in sql.execute(f"SELECT * FROM users WHERE user_id = {user_id}"):
        global column
        column = i
    await message.answer(
        str(f"🏠Кабинет инвестора {column[1]}\nID: {column[0]}\n🦄Добро пожаловать домой, {column[1]}!\nВаш уровень: {column[2]}\n🧞 Босс, здесь Вы можете контролировать свой рабочий процесс:\n Проверить баланс\n Проверить и повысить свой уровень\n Проверить и расширить армию Ваших Единорогов"),
        reply_markup=LK_btn)


@dp.message_handler(lambda message: message.text == 'Перейти к уровням')
async def levels(message: types.Message):
    user_id = message.from_user.id
    for i in sql.execute(f"SELECT * FROM users WHERE user_id = {user_id}"):
        global column
        column = i
    await message.answer(
        f"🦄Ваш текущий уровень: {column[2]}",
        reply_markup=level_btn)


@dp.message_handler(lambda message: message.text == 'Вывод')
async def out_MU(message: types.Message):
    keyboard = money_out3
    await message.answer("Подать заявку или вернуться к балансу : ", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == 'Назад к балансу')
async def take_level_MU(message: types.Message):
    for i in sql.execute(f"SELECT balance FROM users WHERE user_id = {message.from_user.id}"):
        balance = i[0]
        balance_message = (
            f"Ваш баланс: *{balance:.2f}*$\n\n"
            "🦄 Повысьте уровень и расширьте армию для большей маржи"
        )
        await message.answer(balance_message, reply_markup=LK_btn_Balance, parse_mode="Markdown")

def is_withdrawal_period_over(last_deposit_date, withdrawal_days):
    current_date = datetime.datetime.now()
    return (current_date - last_deposit_date).days >= withdrawal_days

@dp.message_handler(lambda message: message.text == 'Подать заявку на вывод', state=None)
async def out_Money(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Назад к балансу'))
    await message.answer("Введите сумму вывода:", reply_markup=keyboard)
    await WithdrawalState.amount.set()


@dp.message_handler(state=WithdrawalState.amount)
async def process_amount(message: types.Message, state: FSMContext):
    user_input = message.text.strip()

    if user_input == 'Назад к балансу':
        await state.finish()
        await LK(message)
        return

    if not user_input.isdigit():
        await message.answer("Неправильный формат введенной суммы. Пожалуйста, введите целое число.")
        return

    withdrawal_amount = int(user_input)
    user_id = message.from_user.id

    last_deposit_date_str = sql.execute(f"SELECT deposit_date FROM users WHERE user_id = {user_id}").fetchone()

    if last_deposit_date_str:
        last_deposit_date_str = last_deposit_date_str[0]
        last_deposit_date = datetime.datetime.strptime(last_deposit_date_str, '%Y-%m-%d %H:%M:%S')

        user_level = sql.execute(f"SELECT level FROM users WHERE user_id = {user_id}").fetchone()

        if user_level:
            if user_level[0] == 'Pony':
                withdrawal_days = 40
            elif user_level[0] == 'Horse':
                withdrawal_days = 30
            elif user_level[0] == 'Unicorn':
                withdrawal_days = 25
            elif user_level[0] == 'Magic Unicorn':
                withdrawal_days = 20
            else:
                withdrawal_days = 100

            if is_withdrawal_period_over(last_deposit_date, withdrawal_days):
                balance = sql.execute(f"SELECT balance FROM users WHERE user_id = {user_id}").fetchone()

                if balance and balance[0] >= withdrawal_amount:
                    await message.answer(
                        f"Выберите способ вывода: Ви можете вивести ваш баланс через {withdrawal_days} днів",
                        reply_markup=money_out4)
                    await WithdrawalState.withdrawal_method.set()
                else:
                    await message.answer("У вас недостаточно средств для вывода.")
            else:
                remaining_days = (last_deposit_date + datetime.timedelta(
                    days=withdrawal_days)) - datetime.datetime.now()
                await message.answer(
                    f"Срок вывода средств еще не наступил. Полный срок: {withdrawal_days} дней. Осталось {remaining_days.days} дней.")
        else:
            await message.answer("Нет информации о вашем уровне. Обратитесь к администратору.")
    else:
        await message.answer("Нет информации о последнем пополнении счета. Обратитесь к администратору.")

    await state.update_data(withdrawal_amount=withdrawal_amount)


@dp.message_handler(lambda message: message.text in ["Crypto Bot", "TRC20"], state=WithdrawalState.withdrawal_method)
async def process_withdrawal_method(message: types.Message, state: FSMContext):
    withdrawal_method = message.text
    data = await state.get_data()
    withdrawal_amount = data.get('withdrawal_amount')
    user_id = message.from_user.id

    admin_message = (
        f"Запрос на вывод:\n"
        f"Пользователь: @{message.from_user.username}\n"
        f"Сумма: {withdrawal_amount}$\n"
        f"Способ вывода: {withdrawal_method}"
    )

    balance = sql.execute(f"SELECT balance FROM users WHERE user_id = {user_id}").fetchone()[0]

    if balance >= withdrawal_amount:
        new_balance = balance - withdrawal_amount
        sql.execute(f"UPDATE users SET balance = {new_balance} WHERE user_id = {user_id}")
        db.commit()

        admins = sql.execute("SELECT user_id FROM users WHERE is_admin = 1").fetchall()
        supports = sql.execute("SELECT user_id FROM users WHERE is_support = 1").fetchall()
        recipient_ids = [admin[0] for admin in admins] + [support[0] for support in supports]

        for recipient_id in recipient_ids:
            await bot.send_message(chat_id=recipient_id, text=admin_message)

        await bot.send_message(message.from_user.id, "Ваша завка была принята и передана на рассмотрение.\n"
                                                     "Вы получите уведомление после подтверждения!\n"
                                                     "Unicorn Team")
    else:
        await message.answer("На вашому рахунку недостатньо коштів.")

    await state.finish()
    await message.answer("Вы отправляетесь в меню", reply_markup=LK_btn)

async def set_user_level(user_id, balance):
    if 50 <= balance <= 500:
        new_level = "Pony"
    elif 501 <= balance <= 1500:
        new_level = "Horse"
    elif 1501 <= balance <= 5000:
        new_level = "Unicorn"
    elif 5001 <= balance <= 100000:
        new_level = "Magic Unicorn"
    else:
        new_level = "mini_hourse"

    sql.execute("UPDATE users SET level = ? WHERE user_id = ?", (new_level, user_id))
    db.commit()

async def check_user_levels():
    while True:
        users = sql.execute("SELECT user_id, balance FROM users").fetchall()
        for user in users:
            user_id = user[0]
            balance = user[1]
            await set_user_level(user_id, balance)
            await update_balance_daily()
        await asyncio.sleep(15)# ЧАС ЗМІНИ БАЛАНСУ #############################################################################################################################################


# АДМИНОЧКА 
        

@dp.message_handler(commands=['activate_admin'], state=None)
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    for i in sql.execute(f"SELECT is_admin FROM users WHERE user_id = '{user_id}'"):
        global is_admin
        is_admin = i

    if is_admin[0] != 0:
        await message.answer("Добро пожаловать, вы авторизованы как Админ!", reply_markup = admin_btn)
    else:
        await message.answer("Вы не админ!")

@dp.message_handler(commands=['activate_support'], state=None)
async def process_start_command(message: types.Message):
    user_id = message.from_user.id
    for i in sql.execute(f"SELECT is_support FROM users WHERE user_id = '{user_id}'"):
        global is_admin
        is_admin = i

    print(i[0])
    if is_admin[0] != 0:
        await message.answer("Добро пожаловать, вы авторизованы как Саппорт!", reply_markup = support_btn)
    else:
        await message.answer("Вы не админ!")

@dp.message_handler(lambda message: message.text == 'Выдать баланс', state=None)
async def give_balance(message: types.Message):
    try:
        user_id = message.from_user.id
        for i in sql.execute(f"SELECT is_support, is_admin FROM users WHERE user_id = '{user_id}'"):
            print(i)
            if i[0] != 0 or i[1] != 0:
                await message.answer("Введите айди пользователя:")
                await GivebalanceState.user_id.set()
            else:
                await message.answer("Это админ команда!")
    except:
        await message.answer("Что-то пошло не так")


@dp.message_handler(state=GivebalanceState.user_id)
async def process_give_balance(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['user_id'] = message.text
        await GivebalanceState.next()
        await message.answer("Введите суму к балансу:")
    except:
        await message.answer("Что-то пошло не так")
        await state.finish()


@dp.message_handler(state=GivebalanceState.sum)
async def process_give_balance(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sum'] = message.text

    async with state.proxy() as data:
        try:
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            user_id = data['user_id']
            sum_to_add = int(data['sum'])

            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            sql.execute(f"UPDATE users SET balance = balance + {sum_to_add}, deposit_date = '{current_time}', deposit = '{sum_to_add}' WHERE user_id = {user_id}")

            deposit_info = sql.execute(f"SELECT deposit FROM users WHERE user_id = {user_id}").fetchone()
            id_refferer = sql.execute(f"SELECT id_refferer FROM users WHERE user_id = {user_id}").fetchone()

            if deposit_info and deposit_info[0] is not None and id_refferer and id_refferer[0] is not None:
                try:
                    sql.execute(f"UPDATE users SET count_refs = count_refs + 1 WHERE user_id = {id_refferer[0]}")
                    sql.execute(f"UPDATE users SET unactive_ref = unactive_ref - 1 WHERE user_id = '{id_refferer[0]}'")
                    db.commit()
                except:
                    await message.answer("Что-то пошло не так")
                    await state.finish()

                await state.finish()
                await message.answer("Операция успешна!", reply_markup=admin_btn)
        except:
            await message.answer("Что-то пошло не так")
            await state.finish()

@dp.message_handler(lambda message: message.text == 'Снять баланс', state=None)
async def take_balance(message: types.Message):
    user_id = message.from_user.id
    try:
        for i in sql.execute(f"SELECT is_support, is_admin FROM users WHERE user_id = '{user_id}'"):
            print(i)
            if i[0] != 0 or i[1] != 0:
                await message.answer("Введите айди пользователя:")
                await TakebalanceState.user_id.set()
            else:
                await message.answer("Это админ команда!")
    except:
        await message.answer("Что-то пошло не так")


@dp.message_handler(state=TakebalanceState.user_id)
async def process_take_balance_user_id(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['user_id'] = message.text
        await TakebalanceState.next()
        await message.answer("Введите разницу к балансу:")
    except:
        await message.answer("Что-то пошло не так")
        await state.finish()

@dp.message_handler(state=TakebalanceState.sum)
async def process_take_balance_sum(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['sum'] = message.text

        async with state.proxy() as data:
            try:
                current_time1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for i in sql.execute(f"SELECT balance FROM users WHERE user_id = '{data['user_id']}'"):
                    last_sum = int(i[0]) - int(data['sum'])
                    sql.execute(f"UPDATE users SET balance = '{last_sum}', last_withdrawal_date = '{current_time1}' WHERE user_id = '{data['user_id']}'")
                    await state.finish()
                    await message.answer("Операция успешна!", reply_markup=admin_btn)
            except:
                await message.answer("Что-то пошло не так")
                await state.finish()
    except:
        await message.answer("Что-то пошло не так")
        await state.finish()

@dp.message_handler(lambda message: message.text == 'Изменить баланс', state=None)
async def change_balance(message: types.Message):
    try:
        user_id = message.from_user.id
        for i in sql.execute(f"SELECT is_support, is_admin FROM users WHERE user_id = '{user_id}'"):
            print(i)
            if i[0] != 0 or i[1] != 0:
                await message.answer("Введите айди пользователя:")
                await ChangebalanceState.user_id.set()
            else:
                await message.answer("Это админ команда!")
    except:
        await message.answer("Что-то пошло не так")

@dp.message_handler(state=ChangebalanceState.user_id)
async def process_change_balance(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['user_id'] = message.text
        await ChangebalanceState.next()
        await message.answer("Введите новый баланс:")
    except:
        await message.answer("Что-то пошло не так")
        await state.finish()

@dp.message_handler(state=ChangebalanceState.sum)
async def process_take_balance(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['sum'] = message.text

        async with state.proxy() as data:
            last_sum = data['sum']
            sql.execute(f"UPDATE users SET balance = '{last_sum}' WHERE user_id = '{data['user_id']}'")
            await state.finish()
            await message.answer("Операция успешна!", reply_markup = admin_btn)
    except:
        await message.answer("Что-то пошло не так")
        await state.finish()

@dp.message_handler(lambda message: message.text == 'Добавить саппорта', state=None)
async def take_balance(message: types.Message):
    user_id = message.from_user.id
    try:
        for i in sql.execute(f"SELECT is_admin FROM users WHERE user_id = '{user_id}'"):
            print(i)
            if i[0] != 0:
                await message.answer("Введите айди пользователя:")
                await MakeadminState.user_id.set()
            else:
                await message.answer("Это админ команда!")
    except:
        await message.answer("Что-то пошло не так")
        await state.finish()

@dp.message_handler(state=MakeadminState.user_id)
async def process_change_balance(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['user_id'] = message.text

        async with state.proxy() as data:
            sql.execute(f"UPDATE users SET is_support = '1' WHERE user_id = '{data['user_id']}'")
            await state.finish()
            await message.answer("Операция успешна!", reply_markup = admin_btn)
    except:
        await message.answer("Что-то пошло не так")
        await state.finish()

@dp.message_handler(lambda message: message.text == 'Снять саппорта', state=None)
async def take_balance(message: types.Message):
    try:
        user_id = message.from_user.id
        for i in sql.execute(f"SELECTis_admin FROM users WHERE user_id = '{user_id}'"):
            print(i)
            if i[0] != 0:
                await message.answer("Введите айди пользователя:")
                await TakeadminState.user_id.set()
            else:
                await message.answer("Это админ команда!")
    except:
        await message.answer("Что-то пошло не так")

@dp.message_handler(state=TakeadminState.user_id)
async def process_change_balance(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['user_id'] = message.text

        async with state.proxy() as data:
            sql.execute(f"UPDATE users SET is_support = '0' WHERE user_id = '{data['user_id']}'")
            await state.finish()
            await message.answer("Операция успешна!", reply_markup = admin_btn)
    except:
        await message.answer("Что-то пошло не так")
        await state.finish()


@dp.message_handler(lambda message: message.text == 'Статистика')
async def take_balance(message: types.Message):
    try:
        user_id = message.from_user.id
        for i in sql.execute(f"SELECT is_admin FROM users WHERE user_id = '{user_id}'"):
            print(i)
            if i[0] != 0:
                users_list = []
                for row in sql.execute(f"SELECT * FROM users"):
                    users_list.append(row)
                users_info = "\n".join([f"ID: {user[0]}, Имя: {user[1]}, Баланс: {user[2]}" for user in users_list])
                total_users = len(users_list)
                await message.answer(f"Всего пользователей: {total_users}\n\nСписок пользователей:\n{users_info}\n\nОтправьте ID пользователя для получения подробной информации о нем.")
            else:
                await message.answer("Это админ команда!")
    except:
        await message.answer("Что-то пошло не так")

@dp.message_handler(lambda message: message.text.isdigit())
async def get_user_info(message: types.Message):
        user_id = message.from_user.id
        for i in sql.execute(f"SELECT is_admin FROM users WHERE user_id = '{user_id}'"):
            print(i)
            if i[0] != 0:
                user_id = int(message.text)
                user_info = sql.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()
                if user_info:
                    await message.answer(f"Информация о пользователе:\nID: {user_info[0]}\nИмя: {user_info[1]}\nБаланс: {user_info[3]}\nДепозит: {user_info[10]}\nЗаработал: {int(user_info[3]) - int(user_info[10])}")
                else:
                    await message.answer("Пользователь с таким ID не найден.")
            else:
                await message.answer("Это админ команда!")


#===============================================================#

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(check_user_levels())
    executor.start_polling(dp, skip_updates=True)