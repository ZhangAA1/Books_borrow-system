import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-2026'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
   # 分页每页数量
    ITEMS_PER_PAGE = 5
    # 借阅期限（天）
    BORROW_DAYS = 30
    # 最大借阅数量
    MAX_BORROW = 5
    # 续借次数
    MAX_RENEW_COUNT = 1
    # 续借延长天数
    RENEW_DAYS = 15