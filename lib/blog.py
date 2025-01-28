import sqlite3
from datetime import datetime
import uuid 
import argparse
import math
import os
import sys
from pathlib import Path
import tzlocal
import difflib

class Blog:
    def __init__(self, db_name='blog', limit = 50, page = 1, sort = 'DESC', soft_deletion = False):
        self.limit = int(limit)
        self.page = int(page)
        self.sort = sort
        self.db_name = 'db/' + Path(db_name).stem + '.db'
        self.soft_deletion = soft_deletion
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        self.create_posts_table()
        self.create_posts_log_table()
        self.add_column('title', 'TEXT')
        self.add_column('deleted', 'INTEGER DEFAULT 0')

    def set_page(self, page):
        self.page = page

    def create_posts_table(self):
        """Создаёт таблицу для записей блога, если она не существует."""
        query = """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT NOT NULL UNIQUE,
            date TEXT NOT NULL,
            last_update TEXT NOT NULL,
            title TEXT,
            content TEXT NOT NULL,
            tags TEXT,
            deleted INTEGER DEFAULT 0,
            timezone TEXT
        );
        """
        self.conn.execute(query)
        self.conn.commit()
        
    def create_posts_log_table(self):
        """Создаёт таблицу для лога."""
        query = """
        CREATE TABLE IF NOT EXISTS posts_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uuid TEXT NOT NULL UNIQUE,
            date TEXT NOT NULL,
            action TEXT NOT NULL,
            post_id INTEGER,
            post_uuid TEXT,
            timezone TEXT
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_log_record(self, post_id, post_uuid, action):
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timezone = tzlocal.get_localzone_name()
        log_record_uuid = str(uuid.uuid4())  # Генерируем UUID
        query = "INSERT INTO posts_log (uuid, date, action, post_id, post_uuid, timezone) VALUES (?, ?, ?, ?, ?, ?)"
        cursor = self.conn.cursor()
        cursor.execute(query, (log_record_uuid, date, action, post_id, post_uuid, timezone))
        self.conn.commit()
        return cursor.lastrowid
        
    def add_column(self, column_name, column_type):
        """
        Добавляет поле column_name к существующей таблице posts, если оно еще не существует.
        """
        try:
            # Проверяем, существует ли поле column_name
            cursor = self.conn.cursor()
            cursor.execute("PRAGMA table_info(posts)")
            columns = cursor.fetchall()
            column_names = [column[1] for column in columns]  # Получаем список имен столбцов

            if column_name not in column_names:
                cursor.execute(f"ALTER TABLE posts ADD COLUMN {column_name} {column_type}")
                self.conn.commit()
                #print(f"Поле '{column_name}' успешно добавлено в таблицу 'posts'.")
            #else:
                #print(f"Поле '{column_name}' уже существует в таблице 'posts'.")

        except sqlite3.Error as e:
            print(f"Ошибка при добавлении поля '{column_name}': {e}")

    def add_post(self, title, content, tags = ""):
        """Добавляет новую запись в блог."""
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        timezone = tzlocal.get_localzone_name()
        post_uuid = str(uuid.uuid4())  # Генерируем UUID
        query = "INSERT INTO posts (uuid, date, title, content, tags, last_update, timezone, deleted) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        cursor = self.conn.cursor()
        cursor.execute(query, (post_uuid, date, title, content, tags, date, timezone, 0))
        self.conn.commit()
        #print("Запись " + str(cursor.lastrowid) + " успешно добавлена!")
        post = self.get_post_by_id(cursor.lastrowid)
        self.add_log_record(post['id'], post['uuid'], 'add')
        return post


    def edit_post(self, post_id, new_title=None, new_content=None, new_tags=None):
        """
        Редактирует текст записи и/или теги по её ID и обновляет поле last_update.
        :param post_id: ID записи, которую нужно отредактировать.
        :param new_content: Новый текст записи (если None, текст не изменяется).
        :param new_tags: Новые теги (если None, теги не изменяются).
        """
        original_post = self.get_post_by_id(post_id)
        last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if new_title is not None and new_content is not None and new_tags is not None:
            query = "UPDATE posts SET title = ?, content = ?, tags = ?, last_update = ? WHERE id = ?"
            self.conn.execute(query, (new_title, new_content, new_tags, last_update, post_id))
        elif new_title is not None and new_content is not None:
            query = "UPDATE posts SET title = ?, content = ?, last_update = ? WHERE id = ?"
            self.conn.execute(query, (new_title, new_content, last_update, post_id))
        elif new_content is not None and new_tags is not None:
            query = "UPDATE posts SET content = ?, tags = ?, last_update = ? WHERE id = ?"
            self.conn.execute(query, (new_content, new_tags, last_update, post_id))
        elif new_title is not None and new_tags is not None:
            query = "UPDATE posts SET title = ?, tags = ?, last_update = ? WHERE id = ?"
            self.conn.execute(query, (new_title, new_tags, last_update, post_id))
        elif new_title is not None:
            query = "UPDATE posts SET title = ?, last_update = ? WHERE id = ?"
            self.conn.execute(query, (new_title, last_update, post_id))
        elif new_content is not None:
            query = "UPDATE posts SET content = ?, last_update = ? WHERE id = ?"
            self.conn.execute(query, (new_content, last_update, post_id))
        elif new_tags is not None:
            query = "UPDATE posts SET tags = ?, last_update = ? WHERE id = ?"
            self.conn.execute(query, (new_tags, last_update, post_id))
        else:
            print("Не указаны новые данные для обновления.")
            return
        self.conn.commit()
        post = self.get_post_by_id(post_id)
        self.add_log_record(post['id'], post['uuid'], 'edit')
        return post

    def edit_post_by_uuid(self, post_uuid, new_content=None, new_tags=None):
        return edit_post(self.get_post_by_uuid(post_uuid)['id'], new_content, new_tags)

    def get_all_posts(self):
        """Возвращает все записи из блога."""
        if self.sort != 'ASC' and self.sort != 'DESC':
            self.sort = 'DESC'
        query = "SELECT * FROM posts ORDER BY id " + self.sort
        cursor = self.conn.execute(query)
        posts = cursor.fetchall()
        return posts
        
    def get_all_log_records(self, sort = 'DESC'):
        if sort != 'ASC' and sort != 'DESC':
            sort = 'DESC'
        query = "SELECT * FROM posts_log ORDER BY id " + sort
        cursor = self.conn.execute(query)
        log_records = cursor.fetchall()
        return log_records

    def get_last_post(self):
        """Возвращает все записи из блога."""
        query = "SELECT * FROM posts ORDER BY id DESC LIMIT 1"
        cursor = self.conn.execute(query)
        post = cursor.fetch()
        return post
        
    def get_last_update(self):
        """Возвращает все записи из блога."""
        query = "SELECT * FROM posts_log ORDER BY id DESC LIMIT 1"
        cursor = self.conn.execute(query)
        last_log_record = cursor.fetchone()
        if last_log_record == None:
            return None
        return (last_log_record['date'], last_log_record['timezone'])

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
        if self.sort != 'ASC' and self.sort != 'DESC':
            self.sort = 'DESC'
        offset = (page - 1) * limit
        query = "SELECT * FROM posts ORDER BY id " + self.sort + " LIMIT ? OFFSET ?"
        cursor = self.conn.execute(query, (limit, offset))
        posts = cursor.fetchall()
        return posts

    def get_post_by_id(self, post_id):
        """Возвращает запись по её ID."""
        query = "SELECT * FROM posts WHERE id = ?"
        """Запятая после post_id нужна для того, чтобы передавлся кортеж"""
        cursor = self.conn.execute(query, (post_id,))
        post = cursor.fetchone()
        return post

    def get_post_by_uuid(self, post_uuid):
        """Возвращает запись по её UUID."""
        query = "SELECT * FROM posts WHERE uuid = ?"
        """Запятая после post_uuid нужна для того, чтобы передавлся кортеж"""
        cursor = self.conn.execute(query, (post_uuid,))
        post = cursor.fetchone()
        return post

    def search_posts(self, search_text = None, search_tags = None):
        """Ищет записи, содержащие указанный текст."""
        if self.sort != 'ASC' and self.sort != 'DESC':
            self.sort = 'DESC'
        if search_text != None and search_tags == None:
            return self.search_posts_by_text(self, search_text)
        elif search_text == None and search_tags != None:
            return self.search_posts_by_tag(self, search_tags)
        elif search_text != None and search_tags != None:
            query = "SELECT * FROM posts WHERE (title LIKE ? OR content LIKE ?) AND tags LIKE ? ORDER BY id " + self.sort + ""
            cursor = self.conn.execute(query, (f'%{search_text}%',f'%{search_text}%',f'%{search_tags}%'))
            return cursor.fetchall()

    def search_posts_by_text(self, search_text):
        """Ищет записи, содержащие указанный текст."""
        if self.sort != 'ASC' and self.sort != 'DESC':
            self.sort = 'DESC'
        query = "SELECT * FROM posts WHERE title LIKE ? OR content LIKE ? ORDER BY id " + self.sort + ""
        cursor = self.conn.execute(query, (f'%{search_text}%', f'%{search_text}%'))
        posts = cursor.fetchall()
        return posts

    def search_posts_by_title(self, search_title):
        """Ищет записи, содержащие указанный текст."""
        if self.sort != 'ASC' and self.sort != 'DESC':
            self.sort = 'DESC'
        query = "SELECT * FROM posts WHERE title LIKE ? ORDER BY id " + self.sort + ""
        cursor = self.conn.execute(query, (f'%{search_title}%'))
        posts = cursor.fetchall()
        return posts
        
    def search_posts_by_tag(self, tag):
        """
        Ищет записи, содержащие указанный тег.
        :param tag: Тег для поиска.
        :return: Список записей, содержащих указанный тег.
        """
        if self.sort != 'ASC' and self.sort != 'DESC':
            self.sort = 'DESC'
        query = "SELECT * FROM posts WHERE tags LIKE ? ORDER BY id " + self.sort + ""
        cursor = self.conn.execute(query, (f'%{tag}%',))
        posts = cursor.fetchall()
        return posts

    def delete_post(self, post_id):
        """Удаляет запись по её ID."""
        post = self.get_post_by_id(post_id)
        if self.soft_deletion == True:
            last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = "UPDATE posts SET deleted = ?, last_update = ? WHERE id = ?"
            self.conn.execute(query, (1, last_update, post_id))
            self.add_log_record(post['id'], post['uuid'], 'soft delete')
        else:
            query = "DELETE FROM posts WHERE id = ?"
            """Запятая после post_id нужна для того, чтобы передавлся кортеж"""
            self.conn.execute(query, (post_id,))
            self.conn.commit()
            self.add_log_record(post['id'], post['uuid'], 'delete')
        return True
        #print(f"Запись с ID {post_id} удалена.")
        
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
        query = "SELECT COUNT(*) FROM posts WHERE deleted = 0"
        cursor = self.conn.execute(query)
        total_posts = cursor.fetchone()[0]
        return total_posts

    def get_current_page(self):
        return self.page

    def close(self):
        """Закрывает соединение с базой данных."""
        self.conn.close()

