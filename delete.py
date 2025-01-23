from blog import Blog
import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser("python " + sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n", "--name", help="Название блога", type=str, default="blog")
    args = parser.parse_args()
    # Удаляем запись
    blog = Blog(args.name)
    post_id = input('ID удаляемой записи: ')
    post_id = int(post_id)
    blog.delete_post(post_id)

    # Закрываем соединение с базой данных
    blog.close()  
