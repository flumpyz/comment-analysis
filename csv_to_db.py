import csv
import sqlite3
import bot

connection = sqlite3.connect("db.db")
cursor = connection.cursor()

with open("parent_video_comment.csv", "r") as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['comment'], i['author'], i['like_count'], i['published_at']) for i in dr]

cursor.executemany("INSERT INTO Video_comment (id, comment, author, like_count, published_at) VALUES (?, ?, ?, ?, ?);", to_db)
connection.commit()
connection.close()