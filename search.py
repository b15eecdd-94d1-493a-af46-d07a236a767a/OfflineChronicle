from blog import Blog
import argparse
import sys
import textwrap

if __name__ == "__main__":
    parser = argparse.ArgumentParser("python " + sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n", "--name", help="Название блога", type=str, default="blog")
    parser.add_argument("-s", "--sort", help="Сортировка", type=str, choices=["DESC", "ASC"], default="DESC")
    parser.add_argument("-sep", "--separator", help="Разделитель между постами", type=str, default="-" * 40)
    parser.add_argument("-w", "--width", help="Максимальная ширина строки", type=int, default=40)
    args = parser.parse_args()
    # Получаем записи
    blog = Blog(args.name)
    search_text = input('Строка для поиска: ')
    
    posts = blog.search_posts(search_text)
    for post in posts:
        print("|" + args.separator)
        print(f"|ID: {post['id']}:, Дата: {post['date']}")
        print("|" + args.separator)
        content = textwrap.fill(str(post['content']), args.width)
        print("|" + "\n|".join(content.split('\n')))
        print("|" + "-" * 40)
        print("|")
    blog.close() 
