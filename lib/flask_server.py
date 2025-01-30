from flask import Flask, render_template, request, redirect, url_for
from blog import Blog
from datetime import datetime
from zoneinfo import ZoneInfo
import tzlocal
import os
from os import environ
import argparse
import sys
import logging
import socket
from flask import jsonify
if environ.get('log') == 'N':
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

def print_sqlite_rows(rows):
    for row in rows:
        print(dict(row))
        
def sqlite_rows_to_dict(rows):
    new_rows = []
    for row in rows:
        new_rows.append(dict(row))
    return new_rows

app = Flask(__name__, template_folder='../template')
app.config['blogname'] = environ.get('blogname')
app.config['timezone'] = environ.get('timezone')
app.config['limit'] = int(environ.get('limit'))
app.config['sort'] = environ.get('sort')
app.config['design'] = str(environ.get('design'))
app.config['readonly'] = environ.get('readonly')
app.config['localhost'] = environ.get('localhost')
app.config['admin_ip'] = environ.get('admin_ip').split()
app.config['debug'] = environ.get('debug')

@app.route('/',  defaults={'page': 1, 'sort': 'DEFAULT'})
@app.route("/index", defaults={'page': 1, 'sort': 'DEFAULT'})
@app.route('/page/<int:page>', defaults={'sort': 'DEFAULT'})
@app.route('/page/<int:page>/sort/ASC', defaults={'sort': 'ASC'})
@app.route('/page/<int:page>/sort/DESC', defaults={'sort': 'DESC'})
def index(page, sort):
    if app.config['localhost'] == 'Y' and request.remote_addr != '127.0.0.1':
        return render_template("only_localhost.html", ip = request.remote_addr)
    if sort == 'DEFAULT':
        sort = app.config['sort']
    page = int(page)
    limit = int(app.config['limit'])
    blog = Blog(app.config['blogname'], limit, page, sort)
    total_pages = blog.get_total_pages()
    if page == -1:
        blog.set_page(total_pages)
    elif page < -1:
        blog.set_page((total_pages) + (page + 1))
    else:
        blog.set_page(page)
    posts = blog.get_all_posts_with_pagination(limit)
    if len(posts) == 0:
        if blog.page >= 0:
            posts = blog.get_all_posts_with_pagination(limit, total_pages)
        else:
            posts = blog.get_all_posts_with_pagination(limit, 1)
    posts = [dict(post) for post in posts]
    for index_post, post in enumerate(posts):
        if post['timezone'] == None:
            origin_tz = ZoneInfo(tzlocal.get_localzone_name())
        else:
            origin_tz = ZoneInfo(str(post['timezone']))
        dt = datetime.fromisoformat(post['date']).replace(tzinfo=origin_tz)
        if app.config['timezone'] == "local" or app.config['timezone'] == "":
            dt = dt.astimezone(tz=ZoneInfo(tzlocal.get_localzone_name()))
        else: 
            dt = dt.astimezone(tz=ZoneInfo(app.config['timezone']))
        posts[index_post]['date'] = dt
    return render_template("blog_template_" + app.config['design'] + ".html", 
    posts=posts, page=page, sort=sort, total_pages=total_pages, blogname=app.config['blogname'], readonly=app.config['readonly'])
    
@app.route("/add_post", methods=['GET', 'POST'])
def add_post():
    if app.config['localhost'] == 'Y' and request.remote_addr != '127.0.0.1':
        return render_template("only_localhost.html", ip = request.remote_addr)
    if app.config['readonly'] == 'Y':
        return render_template('readonly.html')
    if '0.0.0.0' not in app.config['admin_ip'] and request.remote_addr not in app.config['admin_ip']:
        return render_template('access_denied.html')
    blog = Blog('blog')
    if request.method == 'POST':
        content = request.form['content']
        title = request.form['title']
        # Создаем словарь с данными поста
        post = {
            'title': title,
            'content': content
        }
        
        # Добавляем пост в список
        blog.add_post(post['title'].strip(), post['content'].strip())
        
        # Перенаправляем на главную страницу
        return redirect(url_for('index'))
    
    return render_template('add_post.html')

"""
@app.route("/search", defaults={'page': 1, 'sort': 'DEFAULT'})
def search(search, page, sort):
    if app.config['localhost'] == 'Y' and request.remote_addr != '127.0.0.1':
        return render_template("only_localhost.html", ip = request.remote_addr)
    if sort == 'DEFAULT':
        sort = app.config['sort']
    blog = Blog(app.config['blogname'], limit, page, sort)
    posts = blog.search_posts(request.args.get('text'))
    posts = [dict(post) for post in posts]
    for index_post, post in enumerate(posts):
        if post['timezone'] == None:
            origin_tz = ZoneInfo(tzlocal.get_localzone_name())
        else:
            origin_tz = ZoneInfo(str(post['timezone']))
        dt = datetime.fromisoformat(post['date']).replace(tzinfo=origin_tz)
        if app.config['timezone'] == "local" or app.config['timezone'] == "":
            dt = dt.astimezone(tz=ZoneInfo(tzlocal.get_localzone_name()))
        else: 
            dt = dt.astimezone(tz=ZoneInfo(app.config['timezone']))
        posts[index_post]['date'] = dt
    return render_template("blog_template_" + app.config['design'] + ".html", 
    posts=posts, page=page, sort=sort, total_pages=total_pages, blogname=app.config['blogname'], readonly=app.config['readonly'])
 """
    
@app.route("/my_ip", methods=['GET', 'POST'])
def get_my_ip():
    return render_template('get_my_ip.html', ip = request.remote_addr)

if __name__ == 'main':
    if app.config['debug'] == 'Y':
        app.run(debug=True, port=args.port)
    else:
        app.run(debug=False, port=args.port)
    
    
