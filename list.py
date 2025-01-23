from blog import Blog

if __name__ == "__main__":
    # Получаем все записи
    blog = Blog()
    print("Все записи в блоге:")
    print("===")
    posts = blog.get_all_posts_with_pagination()
    for post in posts:
        print(f"ID: {post['id']}:, Дата: {post['date']} \n{post['content']}")
    print('===')
    print('Количество страниц: ' + str(blog.get_total_pages()))
    print('Количество записей: ' + str(blog.get_total_posts()))
    blog.close() 
