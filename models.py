from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timedelta

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    books = db.relationship('Book', backref='category', lazy=True)

class Book(db.Model):
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

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    real_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True)
    library_card = db.Column(db.String(20), unique=True, nullable=False)
    role = db.Column(db.String(20), default='user')
    max_borrow = db.Column(db.Integer, default=5)
    borrow_records = db.relationship('BorrowRecord', backref='user', lazy=True)

    def is_admin(self):
        return self.role == 'admin'

class BorrowRecord(db.Model):
    __tablename__ = 'borrow_records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, default=datetime.now)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default='borrowed')
    renew_count = db.Column(db.Integer, default=0)

    def renew(self):
        if self.renew_count < 1:
            self.due_date += timedelta(days=15)
            self.renew_count += 1
            return True
        return False

    def is_overdue(self):
        if self.status == 'borrowed' and datetime.now() > self.due_date:
            return True
        return False