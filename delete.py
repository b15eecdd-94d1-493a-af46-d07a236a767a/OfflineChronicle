from lib.blog import Blog
import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser("python3 " + sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n", "--name", help="Название блога", type=str, default="blog")
    parser.add_argument("-sd", "--soft-deletion", help="Мягкое удаление (пост остаётся в базе данных)", choices=['Y', 'N'], type=str, default="N")
    args = parser.parse_args()
    # Удаляем запись
    if args.soft_deletion == 'Y':
        soft_deletion = True
    else:
        soft_deletion = False
    blog = Blog(args.name, soft_deletion = soft_deletion)
    post_id = input('ID удаляемой записи: ')
    post_id = int(post_id)
    blog.delete_post(post_id)
    # Закрываем соединение с базой данных
    blog.close()  
