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
    parser.add_argument("-tz", "--timezone", help="Часовой пояс (local - локальный часовой пояс)", type=str, default="local")
    args = parser.parse_args()
    # Получаем запись
    blog = Blog(args.name)
    log_record_date, log_record_timezone = blog.get_last_update()
    if log_record_timezone == None:
        origin_tz = ZoneInfo(tzlocal.get_localzone_name())
    else:
        origin_tz = ZoneInfo(str(log_record_timezone))
    dt = datetime.fromisoformat(log_record_date).replace(tzinfo=origin_tz)
    if args.timezone == "local" or args.timezone == "":
        dt = dt.astimezone(tz=ZoneInfo(tzlocal.get_localzone_name()))
    else: 
        dt = dt.astimezone(tz=ZoneInfo(args.timezone))
    print(dt)
    blog.close() 
