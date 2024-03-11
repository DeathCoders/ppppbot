from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

#Інлайн кнопка на канал
inlbtn_chanel = InlineKeyboardButton(text="Канал", url="https://t.me/+5pdycvl8iWg5NDUy")
inlbtn = InlineKeyboardMarkup(row_width=2).add(inlbtn_chanel)

#Перевірка на підписку
btn_check = InlineKeyboardButton(text = "Подписался", state = "inlbtn_check")
btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn_check)

#Кнопки меню
menu_btn_SP = KeyboardButton("Служба поддержки")
menu_btn_OC = KeyboardButton("Открытый канал")
menu_btn_LK = KeyboardButton("Личный кабинет")

menu_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(menu_btn_SP, menu_btn_OC, menu_btn_LK)

#Кнопки для ЛК
LK_btn_Balance = KeyboardButton("Баланс")
LK_btn_Levels = KeyboardButton("Уровни")
LK_btn_Ref = KeyboardButton("Армия рефералов")
Lk_btn_exit = KeyboardButton("Назад")

LK_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(LK_btn_Balance, LK_btn_Levels, LK_btn_Ref, Lk_btn_exit)

#Кнопки для балансу
balance_key_exit = KeyboardButton("Назад в кабинет")
output_balance = KeyboardButton("Вывод")
level_steep = KeyboardButton("Перейти к уровням")

money_out = KeyboardButton("Подать заявку на вывод")
LK_btn_Balance = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(balance_key_exit, output_balance, level_steep)

back_to_balance = KeyboardButton("Назад к балансу")
money_out3 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(money_out,back_to_balance)

output_balance_1 = KeyboardButton("Crypto Bot")
output_balance_2 = KeyboardButton("TRC20")
money_out4 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(output_balance_1,output_balance_2)


#Кнопки для рівнів
level_btn_up = KeyboardButton("Повысить уровень")
level_btn_back = KeyboardButton("Назад к личному кабинету")

#Кнопки для рефералів
referal_b1 = KeyboardButton("Пригласить")
referal_b2 = KeyboardButton("Назад к инфо")
referal_b1_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(referal_b1, referal_b2)

level_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(level_btn_up, level_btn_back)

btn_pony = KeyboardButton("Pony")
btn_horse = KeyboardButton("Horse")
btn_unicorn = KeyboardButton("Unicorn")
btn_MU = KeyboardButton("Magic Unicorn")

btn_levelUP = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn_pony, btn_horse, btn_unicorn, btn_MU, level_btn_back)

btn_back_to_levels = KeyboardButton("Назад к уровням")

btn_pony_dep_key = KeyboardButton("Запросить уровень Pony")
btn_pony_dep = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn_pony_dep_key ,btn_back_to_levels)

btn_horse_dep_key = KeyboardButton("Запросить уровень Horse")
btn_horse_dep = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn_horse_dep_key ,btn_back_to_levels)

btn_unicorn_dep_key = KeyboardButton("Запросить уровень Unicorn")
btn_unicorn_dep = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn_unicorn_dep_key ,btn_back_to_levels)

btn_MU_dep_key = KeyboardButton("Запросить уровень Magic Unicorn")
btn_MU_dep = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn_MU_dep_key ,btn_back_to_levels)

give_balance_btn = KeyboardButton("Выдать баланс")
take_balance_btn = KeyboardButton("Снять баланс")
change_balance_btn = KeyboardButton("Изменить баланс")

make_admin = KeyboardButton("Добавить саппорта")
take_admin = KeyboardButton("Снять саппорта")

statistic = KeyboardButton("Статистика")
statistic_user = KeyboardButton("Статистика о пользовате")

admin_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(give_balance_btn, take_balance_btn, change_balance_btn, make_admin, take_admin, statistic)

support_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(give_balance_btn, take_balance_btn, change_balance_btn)

stop_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton("Стоп"))