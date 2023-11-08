import telebot
from telebot import types
import psycopg2
import datetime

nowDate = datetime.date.today()

current_day_of_week = nowDate.weekday()

days_of_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
today = days_of_week[current_day_of_week]

dbConfig = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "motherlode",
    "host": "localhost",
    "port": "5432",
}
conn = psycopg2.connect(**dbConfig)
cursor = conn.cursor()


bot_token = "6635780254:AAGWxKHTqQ6Ei19wCJpwqoCkYZbHqlfURuA"
bot = telebot.TeleBot(bot_token)

subgroup = None
selected_day = None

user_states = {}


keyboardDay = types.ReplyKeyboardMarkup(row_width=3)
groopButton = types.ReplyKeyboardMarkup(row_width=3)

firstPG_button = types.KeyboardButton("Первая подгруппа")
secondPG_button = types.KeyboardButton("Вторая подгруппа")

monday_button = types.KeyboardButton("Понедельник")
tuesday_button = types.KeyboardButton("Вторник")
wednesday_button = types.KeyboardButton("Среда")
thursday_button = types.KeyboardButton("Четверг")
friday_button = types.KeyboardButton("Пятница")
saturday_button = types.KeyboardButton("Суббота")
my_timetable_button = types.KeyboardButton("Мое расписание на неделю")

keyboard = types.ReplyKeyboardMarkup(row_width=2)

groopButton.add(firstPG_button, secondPG_button, my_timetable_button)

keyboardDay.add(monday_button, tuesday_button, wednesday_button, thursday_button, friday_button, saturday_button)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Здавствуйте, здесь вы можете получить расписание занятий для любой подгруппы и дня недели.")
    bot.send_message(message.chat.id, "Подгруппа:", reply_markup=groopButton)

@bot.message_handler(commands=['help'])
def help(message):
    help_text = """
    Вы можете использовать следующие команды:
    /week - Узнать какая сейчас неделя
    \n
    /tomorrow - Расписание на завтра
    \n
    /today - Расписание на сегодня
    \n
    /surgu - Официальный сайт СурГУ
    """
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['today'])
def todays(message):
    if subgroup:
        schedule = getSchedule(subgroup, today, message)
        if schedule:
            bot.send_message(message.chat.id, schedule)

    else:
         bot.send_message(message.chat.id, "Выберите подгруппу")


@bot.message_handler(commands=['tomorrow'])
def tomorrows(message):
    if subgroup:
        current_day = datetime.date.today().weekday()
        tomorrow1 = ((current_day + 1) % 7)
        days_of_tomorrow = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        tomorrow = days_of_tomorrow[tomorrow1]
        schedule = getSchedule(subgroup, tomorrow, message)
        if schedule:
            bot.send_message(message.chat.id, schedule)
    else:
         bot.send_message(message.chat.id, "Выберите подгруппу")

@bot.message_handler(commands=['week'])
def week(message):
    if subgroup:
        thisWeek = getThisWeek()
        if thisWeek % 2 == 1:
            bot.send_message(message.chat.id, "Текущая неделя: /Знаменатель (чётная)")
        else:
            bot.send_message(message.chat.id, "Текущая неделя: Числитель\ (нечётная)")


@bot.message_handler(commands=['surgu'])
def Surgu(message):
    bot.send_message(message.chat.id, "Официальный сайт СУРГУ: https://www.surgu.ru/index")

@bot.message_handler(func=lambda message: True, content_types=["text"])
def getmessage(message):
    if message.text == "Вторая подгруппа" or message.text == "Первая подгруппа":

        global subgroup
        if message.text == "Вторая подгруппа":
            subgroup = 2
        else:
            subgroup = 1

        bot.send_message(message.chat.id, "Выберите день недели:", reply_markup=keyboardDay)
    elif message.text in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Мое расписание на неделю"]:

        selectedDay = message.text
        schedule = getSchedule(subgroup, selectedDay, message)
        if schedule:
            bot.send_message(message.chat.id, schedule)



@bot.message_handler(func=lambda message: True, content_types=["text"])
def getSchedule(subgroup, day, message):
    if not day == 'Воскресенье' and day != 'Мое расписание на неделю':

        subgroup = str(subgroup)
        chsznam = str(getThisWeek())

        print(day)

        conn = psycopg2.connect(**dbConfig)
        cursor = conn.cursor()

        sqlQuery = """
            SELECT subject.name, timetable.time, teacher.full_name
            FROM timetable
            INNER JOIN subject ON timetable.subject_id = subject.id
            INNER JOIN teacher ON subject.id = teacher.subject_id
            WHERE timetable.podGroop = %s AND timetable.chsznam = %s AND timetable.day = %s
            ORDER BY timetable.time;  -- Сортировка по времени
        """

        cursor.execute(sqlQuery, (subgroup, chsznam, day))

        scheduleData = cursor.fetchall()

        conn.close()

        formattedSchedule = ""
        if scheduleData:
            formattedSchedule += f"{day}\n"
            currentTime = None
            for row in scheduleData:
                subject, time, teacher = row
                if time != currentTime:
                    formattedSchedule += f"Время: {time}\n"
                    currentTime = time
                formattedSchedule += f"{subject}\n"
                formattedSchedule += f"Преподаватель: {teacher}\n"
        else:
            formattedSchedule = "Расписание не найдено."

        if formattedSchedule:
            bot.send_message(message.chat.id, formattedSchedule)
        else:
            bot.send_message(message.chat.id, "Расписание не найдено.")
    elif day == 'Мое расписание на неделю':

        conn = psycopg2.connect(**dbConfig)
        cursor = conn.cursor()

        sqlQueryData = """
                SELECT * FROM mytimetable
        """

        cursor.execute(sqlQueryData)

        myData = cursor.fetchall()

        print(myData)

        conn.close()

        formatted = ""

        if myData:
            formatted += f"{day}\n"
            for row in myData:
                num, dayofweek, task, tasktime = row
                formatted += f"День недели: {dayofweek}\n"
                formatted += f"Время: {tasktime}\n"
                formatted += f"Задача: {task}\n"
                formatted += "\n"
        else:
            formatted = "Расписание не найдено."

        if formatted:
            bot.send_message(message.chat.id, formatted)
        else:
            bot.send_message(message.chat.id, "Расписание не найдено.")


def getThisWeek():
    todayDate = datetime.date.today()

    startYear = datetime.date(todayDate.year, 9, 1)

    daysDiff = (todayDate - startYear).days

    weeksDiff = daysDiff // 7

    if weeksDiff % 2 == 0:
        return 1
    else:
        return 2

if __name__ == "__main__":
    bot.polling()

conn.close()

print("hello world!")