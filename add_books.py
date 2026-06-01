from app import app, db
from models import Book, Category

books_data = [
    {"title": "三体", "author": "刘慈欣", "isbn": "9787229030931", "publisher": "重庆出版社", "price": 32.0, "total_copies": 5, "category": "文学"},
    {"title": "三体II：黑暗森林", "author": "刘慈欣", "isbn": "9787229030948", "publisher": "重庆出版社", "price": 39.0, "total_copies": 5, "category": "文学"},
    {"title": "三体III：死神永生", "author": "刘慈欣", "isbn": "9787229030955", "publisher": "重庆出版社", "price": 42.0, "total_copies": 5, "category": "文学"},
    {"title": "活着", "author": "余华", "isbn": "9787530211540", "publisher": "作家出版社", "price": 28.0, "total_copies": 4, "category": "文学"},
    {"title": "百年孤独", "author": "加西亚·马尔克斯", "isbn": "9787544253994", "publisher": "南海出版公司", "price": 55.0, "total_copies": 3, "category": "文学"},
    {"title": "Python编程：从入门到实践", "author": "Eric Matthes", "isbn": "9787115428028", "publisher": "人民邮电出版社", "price": 89.0, "total_copies": 6, "category": "科技"},
    {"title": "流畅的Python", "author": "Luciano Ramalho", "isbn": "9787115479316", "publisher": "人民邮电出版社", "price": 139.0, "total_copies": 4, "category": "科技"},
    {"title": "JavaScript高级程序设计", "author": "Nicholas C. Zakas", "isbn": "9787115297976", "publisher": "人民邮电出版社", "price": 99.0, "total_copies": 3, "category": "科技"},
    {"title": "明朝那些事儿", "author": "当年明月", "isbn": "9787213050990", "publisher": "北京联合出版公司", "price": 268.0, "total_copies": 3, "category": "历史"},
    {"title": "人类简史", "author": "尤瓦尔·赫拉利", "isbn": "9787508647357", "publisher": "中信出版社", "price": 68.0, "total_copies": 4, "category": "历史"},
    {"title": "艺术的故事", "author": "贡布里希", "isbn": "9787540274577", "publisher": "广西美术出版社", "price": 280.0, "total_copies": 2, "category": "艺术"},
    {"title": "教育学原理", "author": "王道俊", "isbn": "9787107224898", "publisher": "人民教育出版社", "price": 45.0, "total_copies": 5, "category": "教育"},
    {"title": "小王子", "author": "圣埃克苏佩里", "isbn": "9787532760078", "publisher": "人民文学出版社", "price": 25.0, "total_copies": 4, "category": "少儿"},
    {"title": "哈利·波特与魔法石", "author": "J.K.罗琳", "isbn": "9787020033430", "publisher": "人民文学出版社", "price": 29.0, "total_copies": 4, "category": "少儿"},
]

def add_books():
    with app.app_context():
        category_map = {cat.name: cat for cat in Category.query.all()}
        added_count = 0
        for book_info in books_data:
            existing = Book.query.filter_by(isbn=book_info["isbn"]).first()
            if existing:
                print(f"图书《{book_info['title']}》已存在，跳过")
                continue
            category = category_map.get(book_info["category"])
            if not category:
                print(f"类别 {book_info['category']} 不存在，跳过")
                continue
            book = Book(
                title=book_info["title"],
                author=book_info["author"],
                isbn=book_info["isbn"],
                publisher=book_info["publisher"],
                price=book_info["price"],
                total_copies=book_info["total_copies"],
                available_copies=book_info["total_copies"],
                category_id=category.id
            )
            db.session.add(book)
            added_count += 1
        db.session.commit()
        print(f"成功添加 {added_count} 本新图书，跳过 {len(books_data)-added_count} 本已存在图书")

if __name__ == "__main__":
    add_books()