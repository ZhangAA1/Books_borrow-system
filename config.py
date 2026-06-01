import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-2026'
    SQLALCHEMY_DATABASE_URI = (
        'mssql+pyodbc://@localhost/library_db?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ITEMS_PER_PAGE = 5     #每页展示数量
    BORROW_DAYS = 30       #每次借书时长
    MAX_BORROW = 5         #最大借阅数量
    MAX_RENEW_COUNT = 1    #续借次数
    RENEW_DAYS = 15        #续借天数