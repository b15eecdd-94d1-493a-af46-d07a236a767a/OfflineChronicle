import sqlite3
from datetime import datetime
import uuid 
import argparse
import math
import os
import sys
from pathlib import Path
import tzlocal

class Blog:
    def __init__(self, db_name='blog', limit = 50, page = 1, sort = 'DESC'):
        self.limit = int(limit)
        self.page = int(page)
        self.sort = sort
        self.db_name = Path(db_name).stem + '.db'
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
            last_update TEXT NOT NULL,
            content TEXT NOT NULL,
            tags TEXT,
            timezone TEXT
        );
        """
        self.conn.execute(query)
        self.conn.commit()
        
    def add_column(self, column_name, column_type):
        """
        Добавляет поле tags к существующей таблице posts, если оно еще не существует.
        """
        try:
            # Проверяем, существует ли поле tags
            cursor = self.conn.cursor()
            cursor.execute("PRAGMA table_info(posts)")
            columns = cursor.fetchall()
            column_names = [column[1] for column in columns]  # Получаем список имен столбцов

            if column_name not in column_names:
                cursor.execute(f"ALTER TABLE posts ADD COLUMN {column_name} {column_type}")
                self.conn.commit()
                print(f"Поле '{column_name}' успешно добавлено в таблицу 'posts'.")
            else:
                print(f"Поле '{column_name}' уже существует в таблице 'posts'.")

        except sqlite3.Error as e:
            print(f"Ошибка при добавлении поля '{column_name}': {e}")

    def add_last_update_column(self):
        self.add_column('tags', 'TEXT')

    def add_last_update_column(self):
        self.add_column('last_update', 'TEXT')

    def add_post(self, content, tags = ""):
        """Добавляет новую запись в блог."""
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timezone = tzlocal.get_localzone_name()
        post_uuid = str(uuid.uuid4())  # Генерируем UUID
        query = "INSERT INTO posts (uuid, date, content, tags, last_update, timezone) VALUES (?, ?, ?, ?, ?, ?)"
        cursor = self.conn.cursor()
        cursor.execute(query, (post_uuid, date, content, tags, date, timezone))
        self.conn.commit()
        #print("Запись успешно добавлена!")
        return cursor.lastrowid


    def edit_post(self, post_id, new_content=None, new_tags=None):
        """
        Редактирует текст записи и/или теги по её ID и обновляет поле last_update.
        :param post_id: ID записи, которую нужно отредактировать.
        :param new_content: Новый текст записи (если None, текст не изменяется).
        :param new_tags: Новые теги (если None, теги не изменяются).
        """
        last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if new_content is not None and new_tags is not None:
            query = "UPDATE posts SET content = ?, tags = ?, last_update = ? WHERE id = ?"
            self.conn.execute(query, (new_content, new_tags, last_update, post_id))
        elif new_content is not None:
            query = "UPDATE posts SET content = ?, last_update = ? WHERE id = ?"
            self.conn.execute(query, (new_content, last_update, post_id))
        elif new_tags is not None:
            query = "UPDATE posts SET tags = ?, last_update = ? WHERE id = ?"
            self.conn.execute(query, (new_tags, last_update, post_id))
        else:
            print("Не указаны новые данные для обновления.")
            return

    def edit_post_by_uuid(self, post_uuid, new_content=None, new_tags=None):
        return edit_post(self.get_post_by_uuid(post_uuid)['id'], new_content, new_tags)

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

    def search_posts(self, search_text = None, search_tags = None):
        """Ищет записи, содержащие указанный текст."""
        if search_text != None and search_tags == None:
            return self.search_posts_by_text(self, search_text)
        elif search_text == None and search_tags != None:
            return self.search_posts_by_tag(self, search_tags)
        elif search_text != None and search_tags != None:
            query = "SELECT * FROM posts WHERE content LIKE ? AND tags LIKE ? ORDER BY id " + self.sort + ""
            cursor = self.conn.execute(query, (f'%{search_text}%',f'%{search_tags}%'))
            return cursor.fetchall()

    def search_posts_by_text(self, search_text):
        """Ищет записи, содержащие указанный текст."""
        query = "SELECT * FROM posts WHERE content LIKE ? ORDER BY id " + self.sort + ""
        cursor = self.conn.execute(query, (f'%{search_text}%',))
        posts = cursor.fetchall()
        return posts

    def search_posts_by_tag(self, tag):
            """
            Ищет записи, содержащие указанный тег.
            :param tag: Тег для поиска.
            :return: Список записей, содержащих указанный тег.
            """
            query = "SELECT * FROM posts WHERE tags LIKE ? ORDER BY date DESC"
            cursor = self.conn.execute(query, (f'%{tag}%',))
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

