from lib.blog import Blog
import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser("python3 " + sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-n", "--name", help="Название блога", type=str, default="blog")
    args = parser.parse_args()
    # Добавляем запись
    blog = Blog(args.name)
    i = 0
    print("Добавьте новую запись. Используйте Ctrl-D или Ctrl-Z (windows) для сохранения.")
    text = []
    while True:
        try:
            if i == 0:
                line = input('Заголовок: ')
            elif i == 1:
                line = input('Содержимое:\n')
            else:
                line = input('')
        except EOFError:
            break
        if line and i > 0:
            text.append(line)
        elif line and i == 0:
            post = blog.add_post(line.strip(), "")
        else:
            break
        if i > 0:
            blog.edit_post(post['id'], new_content = "\n".join(text).strip())
        i += 1
