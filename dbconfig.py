import psycopg2
from psycopg2 import sql
from psycopg2.extras import execute_values

dbConfig = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "motherlode",
    "host": "localhost",
    "port": "5432",
}

conn = psycopg2.connect(**dbConfig)

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS subject CASCADE;")
cursor.execute("DROP TABLE IF EXISTS teacher CASCADE;")
cursor.execute("DROP TABLE IF EXISTS timetable CASCADE;")
cursor.execute("DROP TABLE IF EXISTS mytimetable CASCADE;")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS subject (
        id SERIAL PRIMARY KEY,
        name TEXT UNIQUE
    );
""")

subject_data = [
    				('Элективные дисциплины по физической культуре',),
                    ('Вычислительная математика(лек), У903',),
                    ('Основы предпринимательской деятельности(пр) У505',),
                    ('Теоретические основы электротехники, п/г 1, У301',),
                    ('Дискретная математика(пр), У504',),
                    ('Работа в команде(пр), А414',),
                    ('Теоретические основы электотехники(лек), У708',),
                    ('Вычислительная математика(пр), А304',),
                    ('Информационные технологии, п/г 1, У606',),
                    ('Основы WEB-инжиниринга,(лек), ЭОиДОТ',),
                    ('Основы WEB-инжиниринга,(пр), ЭОиДОТ',),
                    ('ТФКП и интегральные преобразования(лек), У708',),
                    ('ТФКП и интегральные преобразования(пр), У708',),
                    ('Информационные технологии(лек), У704',),
                    ('Мультимедиа технологии(лек), У903',),
                    ('Иностанный язык, п/г 1, У508',),
                    ('Технология программирования, п/г 1, У606',),
					('Дискретная математика(лек), У903',),
					('Теоретические основы электротехники, п/г 2, У301',),
					('Информационные технологии, п/г 2, У606',),
					('Иностанный язык, п/г 2, У508',),
					('Технология программирования, п/г 2, У606',),
					('Технология программирования(лек), У704',),
					('Мультимедиа технологии(пр), п/г 1, А417',),
					('Мультимедиа технологии(пр), п/г 2, А417',),
                    ]

cursor.executemany("INSERT INTO subject (name) VALUES (%s) ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name;", subject_data)

cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'teacher');")
exists = cursor.fetchone()[0]

cursor.execute("""
	CREATE TABLE teacher (
		id SERIAL PRIMARY KEY,
		full_name TEXT,
		subject_id INT,
		FOREIGN KEY (subject_id) REFERENCES subject(id)
	);
""")

teacher_data = [
        ('Пешков А.В.', 1),
        ('Дубовик А.О.', 2),
        ('Цыкура М.Г.', 3),
        ('Бурмистрова Е.А.', 4),
        ('Мухутдинова Д.Р.', 5),
        ('Сафарли М.С.', 6),
        ('Бурмистрова Е.А.', 7),
        ('Дубовик А.О.', 8),
		('Берестин Д.К.', 9),
		('Живайкин Е.А.', 10),
		('Живайкин Е.А.', 11),
		('Гореликов А.В.', 12),
		('Гореликов А.В.', 13),
		('Берестин Д.К.', 14),
		('Морозов Л.Г.', 15),
		('Чеснокова Н.Е.', 16),
		('Берестин Д.К.', 17),
		('Мухутдинова Д.Р.', 18),
		('Бурмистрова Е.А.', 19),
		('Берестин Д.К.', 20),
		('Савш И.Ю.', 21),
		('Берестин Д.К.', 22),
		('Берестин Д.К.', 23),
        ('Морозов Л.Г.', 24),
        ('Морозов Л.Г.', 25),
    ]

cursor.executemany("INSERT INTO teacher (full_name, subject_id) VALUES (%s, %s);", teacher_data)


cursor.execute("""
    CREATE TABLE IF NOT EXISTS timetable (
        id SERIAL PRIMARY KEY,
        day TEXT,
        ChsZnam TEXT,
        podGroop TEXT,
        subject_id INT,
        time TEXT,
        FOREIGN KEY (subject_id) REFERENCES subject(id)
    );
""")

table_data = [
	('Понедельник', 1, 1, 1, "10:30 - 11:50"),
	('Понедельник', 2, 1, 1, "10:30 - 11:50"),
	('Понедельник', 1, 2, 1, "10:30 - 11:50"),
	('Понедельник', 2, 2, 1, "10:30 - 11:50"),

	('Понедельник', 1, 1, 2, "13:20 - 14:40"),
	('Понедельник', 1, 2, 2, "13:20 - 14:40"),

	('Понедельник', 2, 1, 18, "13:20 - 14:40"),
	('Понедельник', 2, 2, 18, "13:20 - 14:40"),

	('Понедельник', 1, 1, 3, "14:50 - 16:10"),
	('Понедельник', 1, 2, 3, "14:50 - 16:10"),
	('Понедельник', 2, 1, 3, "14:50 - 16:10"),
	('Понедельник', 2, 2, 3, "14:50 - 16:10"),


	('Вторник', 1, 1, 4, "10:00 - 11:20"),
	('Вторник', 2, 2, 19, "10:00 - 11:20"),

	('Вторник', 1, 2, 19, "11:30 - 12:50"),
	('Вторник', 2, 2, 19, "11:30 - 12:50"),

	('Вторник', 1, 1, 5, "13:20 - 14:40"),
	('Вторник', 2, 1, 5, "13:20 - 14:40"),
	('Вторник', 1, 2, 5, "13:20 - 14:40"),
	('Вторник', 2, 2, 5, "13:20 - 14:40"),

	('Вторник', 1, 1, 6, "14:50 - 16:10"),
	('Вторник', 2, 1, 6, "14:50 - 16:10"),
	('Вторник', 1, 2, 6, "14:50 - 16:10"),
	('Вторник', 2, 2, 6, "14:50 - 16:10"),

	('Среда', 1, 1, 7, "10:00 - 11:20"),
	('Среда', 1, 2, 7, "10:00 - 11:20"),

	('Среда', 1, 1, 8, "11:30 - 12:50"),
	('Среда', 2, 1, 8, "11:30 - 12:50"),
	('Среда', 1, 2, 8, "11:30 - 12:50"),
	('Среда', 2, 2, 8, "11:30 - 12:50"),

	('Среда', 1, 1, 9, "13:20 - 14:40"),
	('Среда', 2, 1, 9, "13:20 - 14:40"),

	('Среда', 1, 2, 21, "13:20 - 14:40"),
	('Среда', 2, 2, 21, "13:20 - 14:40"),

	('Среда', 1, 1, 10, "14:50 - 16:10"),
	('Среда', 2, 1, 10, "14:50 - 16:10"),
	('Среда', 1, 2, 10, "14:50 - 16:10"),
	('Среда', 2, 2, 10, "14:50 - 16:10"),

	('Среда', 1, 1, 11, "16:20 - 17:40"),
	('Среда', 2, 1, 11, "16:20 - 17:40"),
	('Среда', 1, 2, 11, "16:20 - 17:40"),
	('Среда', 2, 2, 11, "16:20 - 17:40"),

	('Четверг', 1, 1, 1, "10:30 - 11:50"),
	('Четверг', 2, 1, 1, "10:30 - 11:50"),
	('Четверг', 1, 2, 1, "10:30 - 11:50"),
	('Четверг', 2, 2, 1, "10:30 - 11:50"),

	('Четверг', 1, 1, 12, "13:20 - 14:40"),
	('Четверг', 2, 1, 12, "13:20 - 14:40"),
	('Четверг', 1, 2, 12, "13:20 - 14:40"),
	('Четверг', 2, 2, 12, "13:20 - 14:40"),

	('Четверг', 2, 1, 13, "14:50 - 16:10"),
	('Четверг', 2, 2, 13, "14:50 - 16:10"),

	('Пятница', 1, 2, 22, "14:50 - 16:10"),
	('Пятница', 2, 2, 22, "14:50 - 16:10"),

	('Пятница', 1, 1, 14, "16:20 - 17:50"),
	('Пятница', 1, 2, 14, "16:20 - 17:50"),

	('Пятница', 2, 1, 23, "16:20 - 17:50"),
	('Пятница', 2, 2, 23, "16:20 - 17:50"),

	('Пятница', 1, 1, 15, "18:00 - 19:20"),
	('Пятница', 2, 1, 15, "18:00 - 19:20"),
	('Пятница', 1, 2, 15, "18:00 - 19:20"),
	('Пятница', 2, 2, 15, "18:00 - 19:20"),

	('Суббота', 1, 1, 24, "8:30 - 9:50"),
	('Суббота', 2, 1, 24, "8:30 - 9:50"),

	('Суббота', 1, 1, 16, "10:00 - 11:20"),
	('Суббота', 2, 1, 16, "10:00 - 11:20"),

	('Суббота', 1, 1, 17, "11:30 - 12:50"),
	('Суббота', 2, 1, 17, "11:30 - 12:50"),

	('Суббота', 1, 2, 25, "11:30 - 12:50"),
	('Суббота', 2, 2, 25, "11:30 - 12:50"),
]


execute_values(cursor, """
    INSERT INTO timetable (day, ChsZnam, podGroop, subject_id, time)
    VALUES %s;
""", table_data)


cursor.execute(""" CREATE TABLE mytimetable (id SERIAL PRIMARY KEY, dayofweek TEXT, task TEXT, tasktime TEXT );""")

myTimeTableData = [
	('Понедельник', 'Учёба', "09:00-19:00"),
	('Вторник', 'Учёба', "09:00-19:00"),
	('Среда', 'Учёба', "09:00-19:00"),
	('Четверг', 'Учёба', "11:00 - 18:00"),
	('Пятница', 'Учёба', "09:00-19:00"),
	('Суббота', 'Учёба', "09:00-19:00"),
	('Воскресенье', 'Учёба', "08:30-19:00"),
]

cursor.executemany("INSERT INTO mytimetable (dayofweek, task, tasktime) VALUES (%s, %s, %s);", myTimeTableData)

conn.commit()

cursor.close()
conn.close()

print("Программа выполнена с кодом 1")