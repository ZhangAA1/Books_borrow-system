from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from config import Config
from models import db, User, Book, Category, BorrowRecord
from forms import LoginForm, RegisterForm, BookForm, UserForm, SearchForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = '请先登录'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def init_database():
    """初始化数据库：创建表并插入默认数据"""
    db.create_all()
    # 添加默认类别
    if Category.query.count() == 0:
        default_cats = ['文学', '科技', '历史', '艺术', '教育', '少儿']
        for cat in default_cats:
            db.session.add(Category(name=cat))
        db.session.commit()
    # 添加默认管理员
    if User.query.filter_by(username='admin').first() is None:
        admin = User(
            username='admin',
            password='admin123',
            real_name='系统管理员',
            email='admin@library.com',
            library_card='ADMIN001',
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
    # 添加示例图书
    if Book.query.count() == 0:
        category = Category.query.filter_by(name='文学').first()
        if not category:
            category = Category.query.first()
        sample_book = Book(
            title='Python编程从入门到实践',
            author='Eric Matthes',
            isbn='9787115428028',
            publisher='人民邮电出版社',
            price=89.0,
            total_copies=3,
            available_copies=3,
            category_id=category.id
        )
        db.session.add(sample_book)
        db.session.commit()


# 在应用上下文内执行数据库初始化
with app.app_context():
    init_database()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('登录成功！', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('用户名或密码错误', 'danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=form.password.data,
            real_name=form.real_name.data,
            email=form.email.data,
            library_card=form.library_card.data,
            role='user'
        )
        db.session.add(user)
        try:
            db.session.commit()
            flash('注册成功，请登录', 'success')
            return redirect(url_for('login'))
        except IntegrityError as e:
            db.session.rollback()
            # 由于表单已经做了唯一性验证，这里捕获异常仅作为后备提示
            if 'users.email' in str(e.orig):
                flash('该邮箱已被注册，请使用其他邮箱', 'danger')
            elif 'users.library_card' in str(e.orig):
                flash('该借阅证号已被使用，请更换', 'danger')
            else:
                flash('注册失败，请检查信息后重试', 'danger')
    # 如果验证失败，直接返回模板（模板会显示字段错误）
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('已退出登录', 'info')
    return redirect(url_for('index'))


# ---------- 图书管理 ----------
@app.route('/books')
def books():
    page = request.args.get('page', 1, type=int)
    keyword = request.args.get('keyword', '').strip()
    search_type = request.args.get('search_type', 'title')
    
    query = Book.query.join(Category)
    
    if keyword:
        if search_type == 'title':
            query = query.filter(Book.title.contains(keyword))
        elif search_type == 'author':
            query = query.filter(Book.author.contains(keyword))
        elif search_type == 'category':
            query = query.filter(Category.name.contains(keyword))
    
    pagination = query.paginate(page=page, per_page=app.config['ITEMS_PER_PAGE'], error_out=False)
    books = pagination.items
    form = SearchForm(request.args)
    return render_template('books.html', books=books, pagination=pagination, form=form)


@app.route('/book/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if not current_user.is_admin():
        abort(403)
    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            author=form.author.data,
            isbn=form.isbn.data,
            publisher=form.publisher.data,
            price=form.price.data,
            total_copies=form.total_copies.data,
            available_copies=form.available_copies.data,
            category_id=form.category_id.data
        )
        db.session.add(book)
        db.session.commit()
        flash('图书添加成功', 'success')
        return redirect(url_for('books'))
    return render_template('book_form.html', form=form, title='添加图书')


@app.route('/book/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_book(id):
    if not current_user.is_admin():
        abort(403)
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.isbn = form.isbn.data
        book.publisher = form.publisher.data
        book.price = form.price.data
        book.total_copies = form.total_copies.data
        book.available_copies = form.available_copies.data
        book.category_id = form.category_id.data
        db.session.commit()
        flash('图书信息已更新', 'success')
        return redirect(url_for('books'))
    return render_template('book_form.html', form=form, title='编辑图书')


@app.route('/book/delete/<int:id>')
@login_required
def delete_book(id):
    if not current_user.is_admin():
        abort(403)
    book = Book.query.get_or_404(id)
    if BorrowRecord.query.filter_by(book_id=id, status='borrowed').first():
        flash('该图书尚有未归还记录，无法删除', 'danger')
    else:
        db.session.delete(book)
        db.session.commit()
        flash('图书已删除', 'success')
    return redirect(url_for('books'))


# ---------- 用户管理（管理员）----------
@app.route('/users')
@login_required
def users():
    if not current_user.is_admin():
        abort(403)
    page = request.args.get('page', 1, type=int)
    pagination = User.query.paginate(page=page, per_page=app.config['ITEMS_PER_PAGE'], error_out=False)
    users = pagination.items
    return render_template('users.html', users=users, pagination=pagination)


@app.route('/user/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if not current_user.is_admin():
        abort(403)
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password='123456',
            real_name=form.real_name.data,
            email=form.email.data,
            library_card=form.library_card.data,
            role=form.role.data
        )
        db.session.add(user)
        db.session.commit()
        flash('用户添加成功', 'success')
        return redirect(url_for('users'))
    return render_template('user_form.html', form=form, title='添加用户')


@app.route('/user/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if not current_user.is_admin():
        abort(403)
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    form.set_user_id(user.id)  # 新增：用于验证时排除自身
    if form.validate_on_submit():
        user.username = form.username.data
        user.real_name = form.real_name.data
        user.email = form.email.data
        user.library_card = form.library_card.data
        user.role = form.role.data
        db.session.commit()
        flash('用户信息已更新', 'success')
        return redirect(url_for('users'))
    return render_template('user_form.html', form=form, title='编辑用户')


@app.route('/user/delete/<int:id>')
@login_required
def delete_user(id):
    if not current_user.is_admin():
        abort(403)
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('不能删除当前登录用户', 'danger')
        return redirect(url_for('users'))
    # 检查是否有未归还的图书（可选的业务约束）
    if BorrowRecord.query.filter_by(user_id=id, status='borrowed').first():
        flash('该用户有未归还图书，无法删除', 'danger')
    else:
        # 删除该用户的所有借阅记录（已归还的也一并删除，避免外键约束）
        BorrowRecord.query.filter_by(user_id=id).delete()
        db.session.delete(user)
        db.session.commit()
        flash('用户已删除', 'success')
    return redirect(url_for('users'))


# ---------- 借阅管理 ----------
@app.route('/borrow/book/<int:book_id>')
@login_required
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    if book.available_copies <= 0:
        flash('图书库存不足，无法借阅', 'danger')
        return redirect(url_for('books'))
    borrowed_count = BorrowRecord.query.filter_by(user_id=current_user.id, status='borrowed').count()
    if borrowed_count >= current_user.max_borrow:
        flash(f'您已达到最大借阅数量({current_user.max_borrow}本)，无法继续借阅', 'danger')
        return redirect(url_for('books'))
    overdue_records = BorrowRecord.query.filter_by(user_id=current_user.id, status='borrowed').all()
    for record in overdue_records:
        if record.is_overdue():
            flash('您有逾期图书未还，请先归还后再借阅', 'danger')
            return redirect(url_for('my_borrow'))
    due_date = datetime.now() + timedelta(days=app.config['BORROW_DAYS'])
    record = BorrowRecord(
        user_id=current_user.id,
        book_id=book_id,
        due_date=due_date
    )
    book.available_copies -= 1
    db.session.add(record)
    db.session.commit()
    flash(f'成功借阅《{book.title}》，应还日期：{due_date.strftime("%Y-%m-%d")}', 'success')
    return redirect(url_for('my_borrow'))


@app.route('/return/book/<int:record_id>')
@login_required
def return_book(record_id):
    record = BorrowRecord.query.get_or_404(record_id)
    if record.user_id != current_user.id and not current_user.is_admin():
        abort(403)
    if record.status == 'returned':
        flash('该书已归还', 'info')
        return redirect(url_for('my_borrow' if record.user_id == current_user.id else 'borrow_records'))
    record.return_date = datetime.now()
    record.status = 'returned'
    book = Book.query.get(record.book_id)
    book.available_copies += 1
    db.session.commit()
    flash('图书归还成功', 'success')
    if current_user.is_admin():
        return redirect(url_for('borrow_records'))
    return redirect(url_for('my_borrow'))


@app.route('/renew/book/<int:record_id>')
@login_required
def renew_book(record_id):
    record = BorrowRecord.query.get_or_404(record_id)
    if record.user_id != current_user.id:
        abort(403)
    if record.status == 'returned':
        flash('已归还的图书不能续借', 'danger')
        return redirect(url_for('my_borrow'))
    if record.renew():
        db.session.commit()
        flash(f'续借成功，新应还日期：{record.due_date.strftime("%Y-%m-%d")}', 'success')
    else:
        flash('续借次数已达上限', 'danger')
    return redirect(url_for('my_borrow'))


@app.route('/my_borrow')
@login_required
def my_borrow():
    records = BorrowRecord.query.filter_by(user_id=current_user.id).order_by(BorrowRecord.borrow_date.desc()).all()
    return render_template('my_borrow.html', records=records)


@app.route('/borrow_records')
@login_required
def borrow_records():
    if not current_user.is_admin():
        abort(403)
    page = request.args.get('page', 1, type=int)
    pagination = BorrowRecord.query.order_by(BorrowRecord.borrow_date.desc()).paginate(
        page=page, per_page=app.config['ITEMS_PER_PAGE'], error_out=False
    )
    records = pagination.items
    return render_template('borrow_records.html', records=records, pagination=pagination)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)