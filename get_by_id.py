from blog import Blog

if __name__ == "__main__":
    # Получаем запись
    blog = Blog()
    post_id = int(input('ID поста: '))
    
    post = blog.search_by_id(post_id)
    print(f"ID: {post['id']}:, Дата: {post['date']} \n {post['content']}")
    blog.close() 
