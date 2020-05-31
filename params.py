import json

params={}

days_of_week_dict = {
                   "mon": "Понедельник",
                   "tue": "Вторник",
                   "wed": "Среда",
                   "thu": "Четверг",
                   "fri": "Пятница",
                   "sat": "Суббота",
                   "sun": "Воскресенье",
}

time_amount_dict = dict([
("key1", "1-2 часа в неделю"),
("key2", "3-5 часов в неделю"),
("key3", "5-7 часов в неделю"),
("key4", "7-10 часов в неделю"),
])

with open('data/goals.json') as json_file:
    goals = json.load(json_file)


import gunicorn