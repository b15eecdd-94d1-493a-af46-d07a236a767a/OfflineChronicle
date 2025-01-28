from lib.blog import Blog
import argparse
import sys
import textwrap

if __name__ == "__main__":
    parser = argparse.ArgumentParser("python3 " + sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n", "--name", help="Название блога", type=str, default="blog")
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
    # Получаем запись
    blog = Blog(args.name)
    post_uuid = int(input('UUID поста: '))
    post = blog.get_post_by_uuid(post_id)
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
    if args.graphics == 'Y':
        print(left_border + args.separator)
    if args.hide_id == 'Y':
        print(f"{left_border}{dt}")
    else:
        print(f"{left_border}ID: {post['id']}, Дата: {dt}")
    if args.graphics == 'Y':
        print(left_border + args.separator)
    content = textwrap.fill(str(post['content']), args.width)
    print(left_border + "\n{left_border}".join(content.split('\n')))
    if args.graphics == 'Y':
        print(left_border + args.separator)
    blog.close() 
