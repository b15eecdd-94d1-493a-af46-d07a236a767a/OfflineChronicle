from blog import Blog
import argparse
import sys
import textwrap
from datetime import datetime
from zoneinfo import ZoneInfo
import tzlocal

if __name__ == "__main__":
    parser = argparse.ArgumentParser("python " + sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n", "--name", help="Название блога", type=str, default="blog")
    parser.add_argument("-l", "--limit", help="Максимальное количество записей", type=int, default=50)
    parser.add_argument("-p", "--page", help="Номер страницы", type=int, default=-1)
    parser.add_argument("-s", "--sort", help="Сортировка", type=str, choices=["DESC", "ASC"], default="ASC")
    parser.add_argument("-sep", "--separator", help="Разделитель между постами", type=str, default="-" * 40)
    parser.add_argument("-w", "--width", help="Максимальная ширина строки", type=int, default=40)
    parser.add_argument("-tz", "--timezone", help="Часовой пояс (local - локальный часовой пояс)", type=str, default="local")
    args = parser.parse_args()
    # Получаем все записи
    blog = Blog(args.name, args.limit, args.page, args.sort)
    total_pages = blog.get_total_pages()
    if args.page == -1:
        blog.set_page(total_pages)
    elif args.page < -1:
        blog.set_page((total_pages) + (args.page + 1))
    else:
        blog.set_page(args.page)
    posts = blog.get_all_posts_with_pagination(args.limit)
    if len(posts) == 0:
        if args.page >= 0:
            posts = blog.get_all_posts_with_pagination(args.limit, total_pages)
        else:
            posts = blog.get_all_posts_with_pagination(args.limit, 1)
    for post in posts:
        print("|" + args.separator)
        if post['timezone'] == None:
            origin_tz = ZoneInfo(tzlocal.get_localzone_name())
        else:
            origin_tz = ZoneInfo(str(post['timezone']))
        dt = datetime.fromisoformat(post['date']).replace(tzinfo=origin_tz)
        if args.timezone == "local" or args.timezone == "":
            dt = dt.astimezone(tz=ZoneInfo(tzlocal.get_localzone_name()))
        else: 
            dt = dt.astimezone(tz=ZoneInfo(args.timezone))
        print(f"|ID: {post['id']}:, Дата: {dt}")
        print("|" + args.separator)
        content = textwrap.fill(str(post['content']), args.width, replace_whitespace = False)
        print("|" + "\n|".join(content.split('\n')))
        print("|" + "-" * 40)
        print("|")
    print('Количество страниц: ' + str(blog.get_total_pages()))
    print('Количество записей: ' + str(blog.get_total_posts()))
    blog.close() 
