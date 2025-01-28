from lib.blog import Blog
import argparse
import sys
import textwrap
from datetime import datetime
from zoneinfo import ZoneInfo
import tzlocal

if __name__ == "__main__":
    parser = argparse.ArgumentParser("python3 " + sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n", "--name", help="Название блога", type=str, default="blog")
    parser.add_argument("-s", "--sort", help="Сортировка", type=str, choices=["DESC", "ASC"], default="DESC")
    parser.add_argument("-sep", "--separator", help="Разделитель между постами", type=str, default="-" * 40)
    parser.add_argument("-lb", "--left-border", help="Граница слева", type=str, default="|")
    parser.add_argument("-g", "--graphics", help="ASCII-графика", type=str, choices=["Y", "N"], default="Y")
    parser.add_argument("-w", "--width", help="Максимальная ширина строки", type=int, default=40)
    parser.add_argument("-tz", "--timezone", help="Часовой пояс (local - локальный часовой пояс)", type=str, default="local")
    parser.add_argument("-hi", "--hide-id", help="Скрыть ID?", type=str, choices=["Y","N"], default="N")
    parser.add_argument("-htz", "--hide-timezone", help="Скрыть часовой пояс?", type=str, choices=["Y","N"], default="N")
    args = parser.parse_args()
    if args.separator == "" and args.left_border == "":
        args.graphics = "N"
    if args.graphics == 'Y':
        left_border = args.left_border
    else:
        left_border = ''
    # Получаем записи
    blog = Blog(args.name, sort=args.sort)
    print('Поиск совершается с учётом регистра символов!')
    search_text = input('Что ищешь? ')
    
    posts = blog.search_posts(search_text)
    
    for post in posts:
        if args.graphics == 'Y':
            print(left_border + args.separator)
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
            print(f"{left_border}{dt}")
        else:
            print(f"{left_border}ID: {post['id']}, Дата: {dt}")
        if args.graphics == 'Y':
            print(f"{left_border}" + args.separator)
        if post['title'] != None and post['title'].strip() != "": 
            print(f"{left_border}" + post['title'])
        content = textwrap.fill(str(post['content']), args.width, replace_whitespace = False)
        print(f"{left_border}" + f"\n{left_border}".join(content.split('\n')))
        if args.graphics == 'Y':
            print(f"{left_border}" + args.separator)
        print(f"{left_border}")
    print('Количество записей: ' + str(len(posts)))
    blog.close() 
