from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

btn_faq = KeyboardButton('FAQ')
btn_pay = KeyboardButton('Оформить подписку')
btn_err = KeyboardButton('Сообщить об ошибке')
btn_back = KeyboardButton('Назад')

main_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

main_menu.add(btn_faq, btn_pay, btn_err)

btn_info = KeyboardButton('Возможности')
btn_comm = KeyboardButton('Список команд')

faq_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

faq_menu.add(btn_info, btn_comm, btn_back)

btn_pay = KeyboardButton('Внести средства')
btn_activ = KeyboardButton('Активировать')

pay_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

pay_menu.add(btn_pay, btn_activ, btn_back)

err_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
err_menu.add(btn_back)