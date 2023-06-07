from db import Database
db = Database('database.db')


async def edit_check(mess, user_id):
    check_status = ""
    task_id = ""

    if mess[-5:-3].isdigit() and mess[-2:].isdigit() and mess[-3] == ":":
        if mess[-8:-6].isdigit() and mess[-11:-9].isdigit() and mess[-16:-12].isdigit() and mess[-9] == "/" and mess[-12] == "/":
            for i in range(len(mess)):
                if mess[i] == " ":
                    break
                else:
                    task_id = task_id + mess[i]
            if task_id.isdigit():
                if db.task_exists(int(task_id)):
                    if db.is_user_task(user_id, task_id):
                        pass
                    else:
                        check_status = "данный id не принадлежит вашей задаче"
                else:
                    check_status = "данный id не существует"
            else:
                check_status = "id введен некоректно"
        else:
            check_status = "Команда должна быть введена в формате: /edit [id] [Описание задачи] [YY/MM/DD] [HH:MM]"
    else:
        check_status = "Команда должна быть введена в формате: /edit [id] [Описание задачи] [YY/MM/DD] [HH:MM]"

    return check_status


async def set_check(mess, user_id):
    check_status = ""
    task_id = ""
    j = 0

    if mess[-5:-3].isdigit() and mess[-2:].isdigit() and mess[-3] == ":":
        if mess[-8:-6].isdigit() and mess[-11:-9].isdigit() and mess[-16:-12].isdigit() and mess[-9] == "/" and mess[-12] == "/":
            for i in range(len(mess)):
                if mess[i] == " ":
                    j = i
                    break
                else:
                    task_id = task_id + mess[i]
            if j == len(mess)-17:
                if task_id.isdigit():
                    if db.task_exists(int(task_id)):
                        if db.is_user_task(user_id, task_id):
                            pass
                        else:
                            check_status = "данный id не принадлежит вашей задаче"
                    else:
                        check_status = "данный id не существует"
                else:
                    check_status = "id введен некоректно"
            else:
                check_status = "Команда должна быть введена в формате: /set [id] [YY/MM/DD] [HH:MM]"
        else:
            check_status = "Команда должна быть введена в формате: /set [id] [YY/MM/DD] [HH:MM]"
    else:
        check_status = "Команда должна быть введена в формате: /set [id] [YY/MM/DD] [HH:MM]"

    return check_status