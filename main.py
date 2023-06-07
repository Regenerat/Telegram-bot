import asyncio
import logging
import err_check

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime, date, time

from menu import main_menu, faq_menu, pay_menu, err_menu
from db import Database

logging.basicConfig(level=logging.INFO)

bot = Bot(token="6000080858:AAEuLGABhzAP2UZmX_2CvalEqV1RW8gP5F4")
PAYMENTS_TOKEN = "401643678:TEST:9b47538d-9d28-48b9-abb7-09f0c260993e"

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database('database.db')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, "Привет", reply_markup=main_menu)


@dp.message_handler(commands=['create'])
async def create(message: types.Message):
    user_task = message.text[8:]
    db.add_task(message.from_user.id, user_task)
    await bot.send_message(message.from_user.id, "Задача успешно создана")


@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    tasks = db.get_tasks(message.from_user.id)
    task_info = ""

    for i in range(0, len(tasks)):
        if tasks[i][4] == "complete":
            task_time = "Время дедлайна: задача уже выполнена"
            task_status = "Статус задачи: Задача была выполнена"
        else:
            task_time = "Время дедлайна: " + str(tasks[i][3])
            task_status = "Статус задачи: Задача не была выполнена"

        if tasks[i][3] is None and tasks[i][4] == "not complete":
            task_time = "Время дедлайна: не назначено"

        task_info = task_info + str(i+1) + f" задача:\n" + "id: " + str(tasks[i][0]) + f"\n" + "Содержание задачи: " + str(tasks[i][2]) + f"\n" + task_time + f"\n" + task_status + f"\n"

    await bot.send_message(message.from_user.id, f"Задачи:\n{task_info}")


@dp.message_handler(commands=['edit'])
async def edit(message: types.Message):
    err = await err_check.edit_check(message.text[6:], message.from_user.id)
    if err == "":
        mess = message.text[6:]
        task_id = ""
        j = 0
        user_id = message.from_user.id

        for i in range(len(mess)):
            if mess[i] == " ":
                j = i + 1
                break
            else:
                task_id = task_id + mess[i]

        task_id = int(task_id)
        user_task = mess[j:-17]

        task_d = int(mess[-8] + mess[-7])
        task_m = int(mess[-11] + mess[-10])
        task_y = int(mess[-16] + mess[-15] + mess[-14] + mess[-13])

        task_h = int(mess[-5] + mess[-4])
        task_min = int(mess[-2] + mess[-1])

        # task_id, user_task, task_date, task_time = map(str, mess.split(' '))
        # task_y, task_m, task_d = map(int, task_date.split('/'))
        # task_h, task_min = map(int, task_time.split(':'))

        task_date = date(task_y, task_m, task_d)
        task_time = time(task_h, task_min)
        task_datatime = datetime.combine(task_date, task_time)

        await db.edit_task(task_id, user_task, task_datatime)
        await bot.send_message(message.from_user.id, f"Задача обновлена")
        await start_task(user_id, task_id)
    else:
        await bot.send_message(message.from_user.id, f"{err}")


@dp.message_handler(commands=['set'])
async def create(message: types.Message):
    err = await err_check.set_check(message.text[5:], message.from_user.id)
    if err == "":
        user_id = message.from_user.id

        mess = message.text[5:]

        task_id, task_date, task_time = map(str, mess.split(' '))
        task_y, task_m, task_d = map(int, task_date.split('/'))
        task_h, task_min = map(int, task_time.split(':'))

        task_date = date(task_y, task_m, task_d)
        task_time = time(task_h, task_min)
        task_datatime = datetime.combine(task_date, task_time)

        await db.set_task(task_id, task_datatime)
        await bot.send_message(message.from_user.id, f'Уведомление установлено')
        await start_task(user_id, task_id)
    else:
        await bot.send_message(message.from_user.id, f"{err}")


async def start_task(user_id, task_id):
    while True:

        if await db.get_time(task_id) is None:
            break

        task_datatime = await db.get_time(task_id)
        task_date, task_time = map(str, task_datatime.split(' '))
        task_y, task_m, task_d = map(int, task_date.split('-'))
        task_h, task_min, task_sec = map(int, task_time.split(':'))

        task_date = date(task_y, task_m, task_d)
        task_time = time(task_h, task_min, task_sec)
        task_datatime = datetime.combine(task_date, task_time)

        curr_time = datetime.now()
        curr_task = await db.get_task(task_id)

        if curr_time.date() == task_datatime.date():
            if curr_time.hour == task_datatime.hour and curr_time.minute == task_datatime.minute:
                await bot.send_message(user_id, f"Вы должны: {curr_task}")
                await db.set_task(task_id, None)
                await db.set_status(task_id)

        await asyncio.sleep(10)


PRICE = types.LabeledPrice(label="Подписка на 1 месяц", amount=500*100)  # в копейках (руб)


async def buy(message: types.Message):
    if PAYMENTS_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, "Тестовый платеж!!!")

    await bot.send_invoice(message.chat.id,
                           title="Подписка на бота",
                           description="Активация подписки на бота на 1 месяц",
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
                           photo_width=416,
                           photo_height=234,
                           photo_size=416,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")


# pre checkout  (must be answered in 10 seconds)
@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


# successful payment
@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await db.set_active(message.from_user.id)
    await bot.send_message(message.chat.id,
                           f"Платеж на сумму {message.successful_payment.total_amount // 100} {message.successful_payment.currency} прошел успешно!!!")


class Form(StatesGroup):
    err = State()


@dp.message_handler(state=Form.err)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['err'] = message.text
        await bot.send_message(355784241, message.text)
    await state.finish()


@dp.message_handler(content_types=['text'])
async def replace_menu(message: types.Message):
    try:
        match message.text:
            case "FAQ":
                await bot.send_message(message.from_user.id, "FAQ", reply_markup=faq_menu)
            case "Оформить подписку":
                await bot.send_message(message.from_user.id, "Оформить подписку", reply_markup=pay_menu)
            case "Сообщить об ошибке":
                await Form.err.set()
                await bot.send_message(message.from_user.id, "Напишите что случилось:", reply_markup=err_menu)
            case "Назад":
                await bot.send_message(message.from_user.id, "Назад", reply_markup=main_menu)
            case "Возможности":
                await bot.send_message(message.from_user.id, "Я ничего не могу(((")
            case "Список команд":
                await bot.send_message(message.from_user.id, f'/create [Описание задачи] - создать новую задачу\n'
                                                             f'/info [id] - предоставить информацию о задачах\n'
                                                             f'/edit [id] [Описание задачи] [YY/MM/DD] [HH:MM] - '
                                                             f'изменить созданную задачу\n'
                                                             f'/set [id] [YY/MM/DD] [HH:MM]- установить дедлайн и '
                                                             f'уведомления\n')
            case "Внести средства":
                await buy(message)
            case "Активировать":
                if await db.is_active(message.from_user.id) == "1":
                    await bot.send_message(message.from_user.id, "Подписка активирована")
                else:
                    await bot.send_message(message.from_user.id, "Вы забылили внести средства")
    except Exception as e:
        print(e)


executor.start_polling(dp)
