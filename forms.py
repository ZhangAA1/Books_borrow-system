from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, FloatField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')

class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    real_name = StringField('真实姓名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[Email()])
    library_card = StringField('借阅证号', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('注册')

    def validate_username(self, field):
        from models import User
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

    def validate_real_name(self, field):
        from models import User
        if User.query.filter_by(real_name=field.data).first():
            raise ValidationError('真实姓名已被注册，请更换')

    def validate_library_card(self, field):
        from models import User
        if User.query.filter_by(library_card=field.data).first():
            raise ValidationError('借阅证号已存在，请更换')

    def validate_email(self, field):
        from models import User
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册，请更换')

class BookForm(FlaskForm):
    title = StringField('书名', validators=[DataRequired()])
    author = StringField('作者', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired()])
    publisher = StringField('出版社')
    price = FloatField('价格', validators=[NumberRange(min=0)])
    total_copies = IntegerField('总册数', validators=[DataRequired(), NumberRange(min=1)])
    available_copies = IntegerField('可借册数', validators=[DataRequired(), NumberRange(min=0)])
    category_id = SelectField('图书类别', coerce=int, validators=[DataRequired()])
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        from models import Category
        self.category_id.choices = [(c.id, c.name) for c in Category.query.all()]

class UserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=3, max=80)])
    real_name = StringField('真实姓名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[Email()])
    library_card = StringField('借阅证号', validators=[DataRequired(), Length(max=20)])
    role = SelectField('角色', choices=[('user', '普通用户'), ('admin', '管理员')], validators=[DataRequired()])
    submit = SubmitField('提交')

    def set_user_id(self, user_id):
        self._user_id = user_id

    def validate_username(self, field):
        from models import User
        query = User.query.filter_by(username=field.data)
        if hasattr(self, '_user_id') and self._user_id:
            query = query.filter(User.id != self._user_id)
        if query.first():
            raise ValidationError('用户名已存在')

    def validate_real_name(self, field):
        from models import User
        query = User.query.filter_by(real_name=field.data)
        if hasattr(self, '_user_id') and self._user_id:
            query = query.filter(User.id != self._user_id)
        if query.first():
            raise ValidationError('真实姓名已被使用')

    def validate_library_card(self, field):
        from models import User
        query = User.query.filter_by(library_card=field.data)
        if hasattr(self, '_user_id') and self._user_id:
            query = query.filter(User.id != self._user_id)
        if query.first():
            raise ValidationError('借阅证号已存在')

    def validate_email(self, field):
        from models import User
        query = User.query.filter_by(email=field.data)
        if hasattr(self, '_user_id') and self._user_id:
            query = query.filter(User.id != self._user_id)
        if query.first():
            raise ValidationError('邮箱已被使用')

class SearchForm(FlaskForm):
    keyword = StringField('关键词')
    search_type = SelectField('搜索类型', choices=[('title', '书名'), ('author', '作者'), ('category', '类别')])
    submit = SubmitField('搜索')