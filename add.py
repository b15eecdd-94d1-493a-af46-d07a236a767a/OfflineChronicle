from blog import Blog

if __name__ == "__main__":
    blog = Blog()
    text = input('Новая запись: \n')
    blog.add_post(text)
