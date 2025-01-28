from lib.blog import Blog
import argparse
import sys
import textwrap
import pprint

if __name__ == "__main__":
    parser = argparse.ArgumentParser("python3 " + sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n", "--name", help="Название блога", type=str, default="blog")
    args = parser.parse_args()
    # Получаем все записи
    blog = Blog(args.name)
    all_log_records = blog.get_all_log_records()
    all_log_records = [dict(log_record) for log_record in all_log_records]
    pprint.pp(all_log_records)
    blog.close() 
