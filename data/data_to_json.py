import json

from data import data

with open('goals.json', 'w', encoding='utf8') as json_file:
    json.dump(data.goals, json_file, ensure_ascii=False)

with open('tutors.json', 'w', encoding='utf8') as json_file:
    json.dump(data.teachers, json_file, ensure_ascii=False)
#
# with open('data/tutors.json') as json_file:
#     tutors = json.load(json_file)