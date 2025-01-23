from blog import Blog

if __name__ == "__main__":
    # Получаем все записи
    blog = Blog()
    search_text = input('Строка для поиска: ')
    
    posts = blog.search_posts(search_text)
    for post in posts:
        print(f"ID: {post['id']}:, Дата: {post['date']} \n {post['content']}")
    blog.close() 
