from blog import Blog
import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser("python " + sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n", "--name", help="Название блога", type=str, default="blog")
    args = parser.parse_args()
    # Добавляем запись
    blog = Blog(args.name)
    i = 0
    print("Добавьте новую запись. Используйте Ctrl-D или Ctrl-Z (windows) для сохранения.")
    text = []
    #blog.add_column('timezone', 'TEXT')
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line:
            text.append(line)
        else:
            break
        if i == 0:
            post_id = blog.add_post("\n".join(text).strip())
        else:
            blog.edit_post(post_id, "\n".join(text).strip())
