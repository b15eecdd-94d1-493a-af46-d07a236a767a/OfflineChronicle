import sqlite3
from datetime import datetime
import uuid 
import argparse
import math
import os
import sys

class Blog:
    def __init__(self, db_name='blog'):
        parser = argparse.ArgumentParser("python " + sys.argv[0] + " [-n]")
        parser.add_argument("-n", "--name", help="Название блога", type=str, default="")
        parser.add_argument("-l", "--limit", help="Максимальное количество записей", type=str, default="")
        parser.add_argument("-p", "--page", help="Номер страницы", type=str, default="")
        parser.add_argument("-s", "--sort", help="Сортировка", type=str, choices=["DESC", "ASC"], default="DESC")
        args = parser.parse_args()
        if args.name != "":
            db_name = args.name
        if args.limit == "":
            self.limit = 50
        if args.page == "":
            self.page = 1
        else:
            self.page = int(args.page)
        self.sort = args.sort
        self.db_name = db_name + '.db'
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        """Создает таблицу для записей блога, если она не существует."""
        query = """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT NOT NULL UNIQUE,
            date TEXT NOT NULL,
            content TEXT NOT NULL
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_post(self, content):
        """Добавляет новую запись в блог."""
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        post_uuid = str(uuid.uuid4())  # Генерируем UUID
        query = "INSERT INTO posts (uuid, date, content) VALUES (?, ?, ?)"
        self.conn.execute(query, (post_uuid, date, content))
        self.conn.commit()
        print("Запись успешно добавлена!")

    def get_all_posts(self):
        """Возвращает все записи из блога."""
        query = "SELECT * FROM posts ORDER BY id DESC"
        cursor = self.conn.execute(query)
        posts = cursor.fetchall()
        return posts

    def get_all_posts_with_pagination(self, limit=None, page=None):
        """
        Возвращает записи с пагинацией.
        :param limit: Количество записей на странице.
        :param page: Номер страницы (начиная с 1).
        :return: Список записей для указанной страницы.
        """
        if limit == None:
            limit = self.limit
        if page == None:
            page = self.page
        offset = (page - 1) * limit
        query = "SELECT * FROM posts ORDER BY id " + self.sort + " LIMIT ? OFFSET ?"
        cursor = self.conn.execute(query, (limit, offset))
        posts = cursor.fetchall()
        return posts

    def get_post_by_id(self, post_id):
        """Возвращает запись по её ID."""
        query = "SELECT * FROM posts WHERE id = ?"
        cursor = self.conn.execute(query, (post_id,))
        post = cursor.fetchone()
        return post

    def get_post_by_uuid(self, post_uuid):
        """Возвращает запись по её UUID."""
        query = "SELECT * FROM posts WHERE uuid = ?"
        cursor = self.conn.execute(query, (post_uuid,))
        post = cursor.fetchone()
        return post

    def search_posts(self, search_text):
        """Ищет записи, содержащие указанный текст."""
        query = "SELECT * FROM posts WHERE content LIKE ? ORDER BY id " + self.sort + ""
        cursor = self.conn.execute(query, (f'%{search_text}%',))
        posts = cursor.fetchall()
        return posts

    def delete_post(self, post_id):
        """Удаляет запись по её ID."""
        query = "DELETE FROM posts WHERE id = ?"
        self.conn.execute(query, (post_id,))
        self.conn.commit()
        print(f"Запись с ID {post_id} удалена.")
        
    def get_total_pages(self, limit = None):
        """
        Возвращает общее количество страниц на основе лимита записей на странице.
        :param limit: Количество записей на странице.
        :return: Общее количество страниц.
        """
        if limit == None:
            limit = self.limit 
        total_posts = self.get_total_posts()
        return math.ceil(total_posts / limit)
    
    def get_total_posts(self):
        """
        Возвращает общее количество записей в блоге.
        :return: Общее количество записей.
        """
        query = "SELECT COUNT(*) FROM posts"
        cursor = self.conn.execute(query)
        total_posts = cursor.fetchone()[0]
        return total_posts

    def get_current_page(self):
        return self.page

    def close(self):
        """Закрывает соединение с базой данных."""
        self.conn.close()

# Пример использования
if __name__ == "__main__":
    blog = Blog()

    # Получаем все записи
    print("Все записи в блоге:")
    posts = blog.get_all_posts()
    for post in posts:
        print(f"ID: {post[0]}, Дата: {post[1]}, Текст: {post[2]}")

    # Закрываем соединение с базой данных
    blog.close() 
