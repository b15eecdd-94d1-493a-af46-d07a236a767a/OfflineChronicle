from blog import Blog

if __name__ == "__main__":
    blog = Blog()
    # Удаляем запись
    post_id = input('ID удаляемой записи: ')
    post_id = int(post_id)
    blog.delete_post(post_id)

    # Закрываем соединение с базой данных
    blog.close()  
