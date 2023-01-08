import sqlite3

with sqlite3.connect("Lessons.db") as db:

    cur = db.cursor()

    query = '''INSERT INTO lessons(topic, exercise_1, count_ex, type) VALUES(
    'Контрольная работа',
    'Переведите "мой папа абрикос" на английский язык;my dad is an apricot',
    '5',
    '2')'''

    query2 = '''UPDATE lessons
                SET exercise_5 = 'Повышенная сложность!
                Переведите "Где мои яйца???!" на английский язык;Where are my eggs???!'
                WHERE topic = 'Контрольная работа' '''

    db.execute(query2)


    db.commit()