import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QScrollArea, QLabel, 
    QPushButton, QMessageBox, QLineEdit, QTextEdit, QSplitter
)
from PyQt6.QtGui import QFont
from lib.blog import Blog
import argparse
from datetime import datetime
from zoneinfo import ZoneInfo
import tzlocal
import os

class BlogApp(QWidget):
    def __init__(self):
        super().__init__()
        self.blog = Blog()
        self.initUI()

    def initUI(self):
        self.setFont(font)
        self.setWindowTitle('Блог')
        self.setGeometry(100, 100, 600, 500)
        # Получаем разрешение экрана
        screen = QApplication.primaryScreen()
        size = screen.size()
        width = size.width()
        height = size.height()
        
        # Рассчитываем координаты для центрирования окна
        x = int((width / 2) - (self.frameGeometry().width() / 2))
        y = int((height / 2) - (self.frameGeometry().height() / 2))
        # Перемещаем окно в рассчитанные координаты
        self.move(x, y)
        # Основной layout
        main_layout = QVBoxLayout()


        # Создаем QSplitter для разделения области ввода и просмотра записей
        splitter = QSplitter()
        splitter.setOrientation(Qt.Orientation.Vertical)  # Вертикальное разделение

        # Верхняя часть: область для добавления новой записи
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText('Введите заголовок записи')
        input_layout.addWidget(self.title_input)

        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText('Введите текст записи')
        input_layout.addWidget(self.content_input)

        self.add_button = QPushButton('Добавить запись')
        self.add_button.clicked.connect(self.add_post)
        input_layout.addWidget(self.add_button)

        # Добавляем верхнюю часть в QSplitter
        splitter.addWidget(input_widget)

        # Нижняя часть: область для просмотра записей
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.posts_container = QWidget()
        self.posts_layout = QVBoxLayout(self.posts_container)
        self.posts_layout.setSpacing(10)

        self.scroll_area.setWidget(self.posts_container)
        splitter.addWidget(self.scroll_area)
        splitter.setSizes([100, 300])
        # Добавляем QSplitter в основной layout
        main_layout.addWidget(splitter)

        # Кнопки для навигации
        buttons_layout = QVBoxLayout()

        self.prev_button = QPushButton('Назад')
        self.prev_button.clicked.connect(self.show_previous_posts)
        buttons_layout.addWidget(self.prev_button)

        self.next_button = QPushButton('Вперед')
        self.next_button.clicked.connect(self.show_next_posts)
        buttons_layout.addWidget(self.next_button)

        main_layout.addLayout(buttons_layout)

        self.setLayout(main_layout)

        self.show_posts(1)

    def show_posts(self, page):
        """Отображает записи на указанной странице."""
        # Очищаем контейнер перед добавлением новых записей
        for i in reversed(range(self.posts_layout.count())):
            self.posts_layout.itemAt(i).widget().setParent(None)

        # Вычисляем диапазон записей для текущей страницы
        self.page = page
        self.limit = args.limit
        self.sort = args.sort
        self.blog = Blog(args.blogname, self.limit, 1, self.sort)
        self.total_pages = self.blog.get_total_pages()
        if self.page == -1:
            self.blog.set_page(self.total_pages)
        elif self.page < -1:
            self.blog.set_page((self.total_pages) + (self.page + 1))
        else:
            self.blog.set_page(self.page)
        self.posts = self.blog.get_all_posts_with_pagination(self.limit)
        if len(self.posts) == 0:
            if self.page >= 0:
                self.posts = self.blog.get_all_posts_with_pagination(self.limit, self.total_pages)
            else:
                self.posts = self.blog.get_all_posts_with_pagination(self.limit, 1)
        self.posts = [dict(post) for post in self.posts]
        for index_post, post in enumerate(self.posts):
            if post['timezone'] == None:
                origin_tz = ZoneInfo(tzlocal.get_localzone_name())
            else:
                origin_tz = ZoneInfo(str(post['timezone']))
            dt = datetime.fromisoformat(post['date']).replace(tzinfo=origin_tz)
            if args.timezone == "local" or args.timezone == "":
                dt = dt.astimezone(tz=ZoneInfo(tzlocal.get_localzone_name()))
            else: 
                dt = dt.astimezone(tz=ZoneInfo(args.timezone))
            self.posts[index_post]['date'] = dt
        # Добавляем записи в контейнер
        #for post in self.posts[start_index:end_index]:
        for post in self.posts:
            post_widget = QWidget()
            post_layout = QVBoxLayout(post_widget)
            
            title_label = QLabel('№' + str(post['id']) + ' ' + str(post['date']))
            if post['title'] != None and post['title'].strip() != "":
                title_label.setText(title_label.text() + '/n' + post['title'])
            title_label.setStyleSheet("font-size: 150%; font-weight: bold;")
            post_layout.addWidget(title_label)

            content_label = QLabel(post['content'])
            content_label.setWordWrap(True)
            content_label.setStyleSheet("font-size: 150%;")
            post_layout.addWidget(content_label)

            self.posts_layout.addWidget(post_widget)

    def show_previous_posts(self):
        """Показывает предыдущие записи."""
        if self.page > 0:
            self.page -= 1
            self.show_posts(self.page)

    def show_next_posts(self):
        """Показывает следующие записи."""
        if self.page < self.total_pages:
            self.page += 1
            self.show_posts(self.page)

    def add_post(self):
        """Добавляет новую запись в блог."""
        title = self.title_input.text()
        content = self.content_input.toPlainText()

        if content:
            self.posts.append({'title': title, 'content': content})
            post_id = self.blog.add_post(title, content)
            self.title_input.clear()
            self.content_input.clear()
            self.show_posts(self.page)  # Обновляем отображение
        else:
            QMessageBox.warning(self, 'Ошибка', 'Текст записи не может быть пустым.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser("python3 " + sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n", "--blogname", help="Название блога", type=str, default="blog")
    parser.add_argument("-tz", "--timezone", help="Часовой пояс (local - локальный часовой пояс)", type=str, default="local")
    parser.add_argument("-l", "--limit", help="Максимальное количество постов на одной странице", type=int, default=50)
    parser.add_argument("-s", "--sort", help="Сортировка", type=str, choices=["DESC", "ASC"], default="DESC")
    parser.add_argument("-p", "--port", help="Порт", type=int, default=5050)
    parser.add_argument("-ro", "--readonly", help="Режим без возможности управлять записями", type=str, choices=["Y", "N"], default="N")
    args = parser.parse_args()
    app = QApplication(sys.argv)
    # Получаем информацию о DPI экрана
    screen = app.primaryScreen()
    dpi = screen.logicalDotsPerInch()
    
    # Масштабируем шрифт в зависимости от DPI
    font_size = int(13 * dpi / 96)  # 96 DPI — стандартное значение
    font = QFont("Arial", font_size)
    app.setFont(font)
    blog_app = BlogApp()
    blog_app.show()
    sys.exit(app.exec())
