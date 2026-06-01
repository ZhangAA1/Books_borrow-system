# 图书借阅管理系统

基于 Flask + SQL Server / SQLite 开发的图书借阅管理系统，支持图书管理、读者管理、借阅/续借/归还、用户权限控制等功能。

## 项目简介

本项目是一个完整的图书借阅管理系统，满足高校图书馆日常管理需求。系统采用 MVC 架构，使用 Flask 轻量级 Web 框架，数据库支持 SQLite（默认）和 SQL Server，具备以下特点：

- 用户角色：管理员和普通读者
- 图书检索：支持按书名、作者、类别多条件搜索，分页显示
- 借阅管理：读者可借阅、续借、归还图书，系统自动校验库存和借阅数量上限
- 用户管理：管理员可增删改查读者信息，支持唯一性验证（用户名、真实姓名、邮箱、借阅证号）
- 数据完整性：数据库设计达到第三范式，包含外键约束和唯一约束
- 安全机制：基于 Flask-Login 的会话管理，不同角色访问权限隔离

## 技术栈

- **后端**：Flask、Flask-SQLAlchemy、Flask-Login、Flask-WTF
- **数据库**：SQLite（默认）/ SQL Server（可选）
- **前端**：Bootstrap 5、Font Awesome
- **语言**：Python 3.9+

## 快速开始

### 环境要求

- Python 3.9 或更高版本
- pip 包管理工具

### 安装步骤

1. **克隆或下载项目**

   ```bash
   git clone https://github.com/your-username/library_system.git
   cd library_system
创建虚拟环境（推荐）

bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
安装依赖

bash
pip install -r requirements.txt
配置数据库

使用 SQLite（默认）：无需额外配置，系统会自动创建 library.db 文件。

使用 SQL Server：请修改 config.py 中的 SQLALCHEMY_DATABASE_URI，例如：

python
SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://sa:password@localhost/library_db?driver=ODBC+Driver+17+for+SQL+Server'
并确保 SQL Server 服务已启动，数据库 library_db 已创建。

初始化数据库

首次运行会自动创建表并插入默认数据（管理员账号、图书类别、示例图书）。

运行应用

bash
python app.py
访问系统

打开浏览器，访问 http://127.0.0.1:5000

默认管理员账号
用户名	密码
admin	admin123
普通用户请通过注册页面自行注册。

功能模块
读者功能
注册/登录

浏览图书（支持按书名、作者、类别搜索和分页）

借阅图书（系统自动校验库存、最大借阅数量、逾期未还限制）

续借图书（最多续借1次，延长15天）

归还图书

查看个人借阅记录

管理员功能
图书管理：增删改查图书，设定分类、库存等

读者管理：增删改查读者，修改角色（管理员/普通用户）

借阅记录：查看所有读者的借阅、归还记录，可强制归还

数据唯一性验证：用户名、真实姓名、邮箱、借阅证号均不可重复

项目结构
text
library_system/
├── app.py                 # Flask 应用主文件
├── config.py              # 配置文件（数据库连接、分页、借阅规则）
├── models.py              # 数据库模型（Category, Book, User, BorrowRecord）
├── forms.py               # WTForms 表单及验证逻辑
├── requirements.txt       # Python 依赖列表
├── add_books.py           # 批量添加图书脚本（可选）
├── templates/             # HTML 模板
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── books.html
│   ├── book_form.html
│   ├── users.html
│   ├── user_form.html
│   ├── my_borrow.html
│   └── borrow_records.html
└── README.md              # 项目说明文档
