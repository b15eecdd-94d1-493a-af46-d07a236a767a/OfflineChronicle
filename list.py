from blog import Blog
import argparse
import sys
import textwrap

if __name__ == "__main__":
    parser = argparse.ArgumentParser("python " + sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n", "--name", help="Название блога", type=str, default="blog")
    parser.add_argument("-l", "--limit", help="Максимальное количество записей", type=int, default=50)
    parser.add_argument("-p", "--page", help="Номер страницы", type=int, default=1)
    parser.add_argument("-s", "--sort", help="Сортировка", type=str, choices=["DESC", "ASC"], default="DESC")
    parser.add_argument("-sep", "--separator", help="Разделитель между постами", type=str, default="-" * 40)
    parser.add_argument("-w", "--width", help="Максимальная ширина строки", type=int, default=40)
    parser.add_argument("-tz", "--timezone", help="Часовой пояс (local - локальный часовой пояс)", type=str, default="local")
    args = parser.parse_args()
    # Получаем все записи
    blog = Blog(args.name, args.limit, args.page, args.sort)
    posts = blog.get_all_posts_with_pagination()
    for post in posts:
        print("|" + args.separator)
        print(f"|ID: {post['id']}:, Дата: {post['date']}")
        print("|" + args.separator)
        content = textwrap.fill(str(post['content']), args.width)
        print("|" + "\n|".join(content.split('\n')))
        print("|" + "-" * 40)
        print("|")
    print('Количество страниц: ' + str(blog.get_total_pages()))
    print('Количество записей: ' + str(blog.get_total_posts()))
    blog.close() 
