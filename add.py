from blog import Blog

if __name__ == "__main__":
    blog = Blog()
    i = 0
    text = input('Новая запись: \n')
    blog.add_post(text)
