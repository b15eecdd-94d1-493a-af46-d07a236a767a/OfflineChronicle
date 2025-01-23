from blog import Blog
import argparse
import sys
import textwrap

if __name__ == "__main__":
    parser = argparse.ArgumentParser("python " + sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n", "--name", help="Название блога", type=str, default="blog")
    parser.add_argument("-sep", "--separator", help="Разделитель между постами", type=str, default="-" * 40)
    parser.add_argument("-w", "--width", help="Максимальная ширина строки", type=int, default=40)
    args = parser.parse_args()
    # Получаем запись
    blog = Blog(args.name)
    post_uuid = input('UUID поста: ')
    
    post = blog.get_post_by_uuid(post_id)
    print("|" + args.separator)
    print(f"|ID: {post['id']}:, Дата: {post['date']}")
    print("|" + args.separator)
    content = textwrap.fill(str(post['content']), args.width)
    print("|" + "\n|".join(content.split('\n')))
    print("|" + "-" * 40)
    blog.close() 
