from blog import Blog

if __name__ == "__main__":
    # Получаем все записи
    blog = Blog()
    post_uuid = input('UUID поста: ')
    
    post = blog.search_by_uuid(post_id)
    print(f"ID: {post['id']}:, Дата: {post['date']} \n {post['content']}")
    blog.close() 
