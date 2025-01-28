from lib.blog import Blog
import argparse
import sys
import textwrap
from datetime import datetime
from zoneinfo import ZoneInfo
import tzlocal
from pathlib import Path
import json
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser("python3 " + sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n", "--name", help="Название блога", type=str, default="blog")
    parser.add_argument("-l", "--limit", help="Максимальное количество записей в одном файле", type=str, default='unlimited')
    parser.add_argument("-s", "--sort", help="Сортировка", type=str, choices=["DESC", "ASC"], default="ASC")
    parser.add_argument("-tz", "--timezone", help="Часовой пояс (local - локальный часовой пояс)", type=str, default="local")
    parser.add_argument("-f", "--format", help="Формат", type=str, choices=['txt', 'json'], default="txt")
    parser.add_argument("-p", "--path", help="Куда сохранять?", type=str, default="export")
    parser.add_argument("-f2", "--force", help="Перезаписывать существующий файл?", type=str, choices=["Y","N"], default="N")
    parser.add_argument("-hi", "--hide-id", help="Скрыть ID в .txt?", type=str, choices=["Y","N"], default="Y")
    parser.add_argument("-htz", "--hide-timezone", help="Скрыть часовой пояс в .txt?", type=str, choices=["Y","N"], default="Y")
    args = parser.parse_args()
    # Получаем все записи
    if args.limit == 'unlimited':
        blog = Blog(args.name, sort = args.sort)
        total_pages = 1
        blog.set_page(1)
        posts = blog.get_all_posts()
    elif args.limit.isdigit():
        blog = Blog(args.name, args.limit, 1, args.sort)
        total_pages = blog.get_total_pages()
        blog.set_page(1)
        posts = blog.get_all_posts_with_pagination(int(args.limit))
        if len(posts) == 0:
            raise Exception("Нету записей.")
    else:
        print('Неправильный limit.')
        sys.exit()
    if not Path(args.path).exists():
        os.makedirs(args.path)
    if args.format == 'txt':
        if args.limit == 'unlimited':
            txt = ''
            i = 0
            for post in posts:
                if i != 0:
                    txt += "\n"
                if post['timezone'] == None:
                    origin_tz = ZoneInfo(tzlocal.get_localzone_name())
                else:
                    origin_tz = ZoneInfo(str(post['timezone']))
                dt = datetime.fromisoformat(post['date']).replace(tzinfo=origin_tz)
                if args.timezone == "local" or args.timezone == "":
                    dt = dt.astimezone(tz=ZoneInfo(tzlocal.get_localzone_name()))
                else: 
                    dt = dt.astimezone(tz=ZoneInfo(args.timezone))
                if args.hide_timezone == 'Y':
                    dt = dt.strftime('%Y-%m-%d %H:%M:%S')
                if args.hide_id == 'Y':
                    txt += f"{dt}\n"
                else:
                    txt += f"ID: {post['id']}, Дата: {dt}"  + "\n"
                if post['title'] != None and post['title'].strip() != "": 
                    txt += post['title'] + "\n"
                txt += post['content'] + "\n"
                i += 1
            export_file_path = args.path + "/" + args.name + ".txt"
            if args.force != 'Y' and Path(export_file_path).exists():
                raise Exception("Файл " + export_file_path + " уже существует, " +
                " используйте флаг --force с параметром Y, если хотите принудительно перезаписать файл.")
            with open(export_file_path, "w", encoding="utf-8") as file:
                file.write(txt)
        else:
            page = 1
            while page < total_pages:
                if page != 1:
                    posts = blog.get_all_posts_with_pagination(int(args.limit), page)
                txt = ''
                i = 0
                for post in posts:
                    if i != 0:
                        txt += "\n\n"
                    if post['timezone'] == None:
                        origin_tz = ZoneInfo(tzlocal.get_localzone_name())
                    else:
                        origin_tz = ZoneInfo(str(post['timezone']))
                    dt = datetime.fromisoformat(post['date']).replace(tzinfo=origin_tz)
                    if args.timezone == "local" or args.timezone == "":
                        dt = dt.astimezone(tz=ZoneInfo(tzlocal.get_localzone_name()))
                    else: 
                        dt = dt.astimezone(tz=ZoneInfo(args.timezone))
                    if args.hide_timezone == 'Y':
                        dt = dt.strftime('%Y-%m-%d %H:%M:%S')
                    if args.hide_id == 'Y':
                        txt += f"{dt}\n"
                    else:
                        txt += f"ID: {post['id']}, Дата: {dt}"  + "\n"
                    if post['title'] != None and post['title'].strip() != "": 
                        txt += post['title'] + "\n"
                    txt += post['content']
                    i += 1
                export_file_path = args.path + "/" + args.name + "_" + str(page) + ".txt"
                if args.force != 'Y' and Path(export_file_path).exists():
                    raise Exception("Файл " + export_file_path + " уже существует, " +
                    " используйте флаг --force с параметром Y, если хотите принудительно перезаписать файл.")
                with open(export_file_path, "w", encoding="utf-8") as file:
                    file.write(txt)
                page += 1
    elif args.format == 'json':
        if args.limit == 'unlimited':
            export_file_path = args.path + "/" + args.name + ".json"
            if args.force != 'Y' and Path(export_file_path).exists():
                raise Exception("Файл " + export_file_path + " уже существует, " +
                " используйте флаг --force с параметром Y, если хотите принудительно перезаписать файл.")
            with open(export_file_path, "w", encoding="utf-8") as file:
                posts = [dict(post) for post in posts]
                file.write(json.dumps(posts, indent=4))
        else:
            i = 1
            while i < total_pages:
                if i != 1:
                    posts = blog.get_all_posts_with_pagination(args.limit, i)
                export_file_path = args.path + "/" + args.name + "_" + i + ".json"
                if args.force != 'Y' and Path(export_file_path).exists():
                    raise Exception("Файл " + export_file_path + " уже существует, " +
                    " используйте флаг --force с параметром Y, если хотите принудительно перезаписать файл.")
                with open(export_file_path, "w", encoding="utf-8") as file:
                    posts = [dict(post) for post in posts]
                    file.write(json.dumps(posts, indent=4))    
                i += 1    
    blog.close() 
