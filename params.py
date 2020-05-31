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

with open('data/goals.json') as json_file:
    goals = json.load(json_file)
