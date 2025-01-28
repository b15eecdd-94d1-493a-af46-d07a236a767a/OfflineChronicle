from lib.blog import Blog
import argparse
import sys
import textwrap
import pprint
from zoneinfo import ZoneInfo
from datetime import datetime
import tzlocal

if __name__ == "__main__":
    parser = argparse.ArgumentParser("python3 " + sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n", "--name", help="Название блога", type=str, default="blog")
    parser.add_argument("-tz", "--timezone", help="Часовой пояс (local - локальный часовой пояс)", type=str, default="local")
    parser.add_argument("-sep", "--separator", help="Разделитель между постами", type=str, default="-" * 40)
    parser.add_argument("-s", "--sort", help="Сортировка", type=str, choices=["DESC", "ASC"], default="ASC")
    args = parser.parse_args()
    # Получаем все записи
    blog = Blog(args.name)
    all_log_records = blog.get_all_log_records(sort = args.sort)
    all_log_records = [dict(log_record) for log_record in all_log_records]
    for log_record in all_log_records:
        print("|" + args.separator)
        if log_record['timezone'] == None:
            origin_tz = ZoneInfo(tzlocal.get_localzone_name())
        else:
            origin_tz = ZoneInfo(str(log_record['timezone']))
        dt = datetime.fromisoformat(log_record['date']).replace(tzinfo=origin_tz)
        if args.timezone == "local" or args.timezone == "":
            dt = dt.astimezone(tz=ZoneInfo(tzlocal.get_localzone_name()))
        else: 
            dt = dt.astimezone(tz=ZoneInfo(args.timezone))
        print(f"|ID: {log_record['id']}, Дата: {dt}")
        print("|" + args.separator)
        print(f"|Событие: " + log_record['action'] + f", пост №{log_record['post_id']}")
        print("|" + args.separator)
        print("|")
    print('Записей: ' + str(len(all_log_records)))
    blog.close() 
