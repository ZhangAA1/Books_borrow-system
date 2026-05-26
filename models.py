from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timedelta

db = SQLAlchemy()

class Category(db.Model):
    """图书类别表"""
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    books = db.relationship('Book', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'

class Book(db.Model):
    """图书表"""
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    publisher = db.Column(db.String(100))
    price = db.Column(db.Float)
    total_copies = db.Column(db.Integer, default=1)
    available_copies = db.Column(db.Integer, default=1)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    borrow_records = db.relationship('BorrowRecord', backref='book', lazy=True)

    def __repr__(self):
        return f'<Book {self.title}>'

class User(UserMixin, db.Model):
    """用户表（读者）"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    real_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True)
    library_card = db.Column(db.String(20), unique=True, nullable=False)  # 借阅证号
    role = db.Column(db.String(20), default='user')  # 'admin' or 'user'
    max_borrow = db.Column(db.Integer, default=5)
    
    borrow_records = db.relationship('BorrowRecord', backref='user', lazy=True)

    def is_admin(self):
        return self.role == 'admin'

class BorrowRecord(db.Model):
    """借阅记录表"""
    __tablename__ = 'borrow_records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.now)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='borrowed')  # borrowed, returned
    renew_count = db.Column(db.Integer, default=0)

    def renew(self):
        """续借操作"""
        if self.renew_count < 1:
            self.due_date += timedelta(days=15)
            self.renew_count += 1
            return True
        return False

    def is_overdue(self):
        """判断是否逾期"""
        if self.status == 'borrowed' and datetime.now() > self.due_date:
            return True
        return False