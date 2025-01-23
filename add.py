from blog import Blog

if __name__ == "__main__":
    blog = Blog()
    i = 0
    print("Добавьте новую запись. Используйте Ctrl-D или Ctrl-Z ( windows ) для сохранения.")
    text = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        text.append(line)
    text = "\n".join(text)
    blog.add_post(text.strip())
