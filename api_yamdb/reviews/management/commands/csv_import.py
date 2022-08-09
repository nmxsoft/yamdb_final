import csv
import sqlite3

from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Импорт заготовленных данных из папки static/data'

    def handle(self, *args, **options):
        with open('static/data/users.csv', newline='') as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=',')
            for row in datareader:
                user = User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    bio=row['bio'],
                    role=row['role']
                )
                user.save()

        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()

        with open('static/data/category.csv', newline='') as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=',')
            to_db = [(i['id'], i['name'], i['slug']) for i in datareader]
        sql = ('INSERT INTO reviews_category (id, name, slug) '
               'VALUES (?, ?, ?);')
        cur.executemany(sql, to_db)

        with open('static/data/genre.csv', newline='') as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=',')
            to_db = [(i['id'], i['name'], i['slug']) for i in datareader]
        sql = 'INSERT INTO reviews_genre (id, name, slug) VALUES (?, ?, ?);'
        cur.executemany(sql, to_db)

        with open('static/data/titles.csv', newline='') as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=',')
            to_db = [
                (
                    i['id'],
                    i['name'],
                    i['year'],
                    i['category']
                ) for i in datareader
            ]
        sql = ('INSERT INTO reviews_title (id, name, year, category_id) '
               'VALUES (?, ?, ?, ?);')
        cur.executemany(sql, to_db)

        with open('static/data/genre_title.csv', newline='') as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=',')
            to_db = [
                (i['id'], i['title_id'], i['genre_id']) for i in datareader
            ]
        sql = ('INSERT INTO reviews_titles_genre (id, titles_id, genre_id) '
               'VALUES (?, ?, ?);')
        cur.executemany(sql, to_db)

        with open('static/data/review.csv', newline='') as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=',')
            to_db = [
                (
                    i['id'],
                    i['title_id'],
                    i['text'],
                    i['author'],
                    i['score'],
                    i['pub_date']
                ) for i in datareader
            ]
        sql = ('INSERT INTO reviews_review (id, title_id, text, author_id, '
               'score, pub_date) VALUES (?, ?, ?, ?, ?, ?);')
        cur.executemany(sql, to_db)

        with open('static/data/comments.csv', newline='') as csvfile:
            datareader = csv.DictReader(csvfile, delimiter=',')
            to_db = [
                (
                    i['id'],
                    i['review_id'],
                    i['text'],
                    i['author'],
                    i['pub_date']
                ) for i in datareader
            ]
        sql = ('INSERT INTO reviews_comment (id, review_id, text, author_id, '
               'pub_date) VALUES (?, ?, ?, ?, ?);')
        cur.executemany(sql, to_db)

        print('data import successfully')
        con.commit()
        con.close()
