import sqlite3
from datetime import datetime
connection = sqlite3.connect("data.db")
sql = connection.cursor()

sql.execute("CREATE TABLE IF NOT EXISTS users "
            "(user_id INTEGER, name TEXT, "
            "phone_number TEXT, reg_date DATETIME);")
sql.execute("CREATE TABLE IF NOT EXISTS products "
            "(pr_id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "pr_name TEXT, pr_price REAL, pr_desc TEXT,"
            "pr_photo TEXT, pr_quantity INTEGER,"
            "reg_date DATETIME);")
sql.execute("CREATE TABLE IF NOT EXISTS cart "
            "(user_id INTEGER, pr_id INTEGER, "
            "pr_name TEXT, pr_count INTEGER, "
            "total_price REAL);")
connection.commit()

def add_user(name, phone_number, user_id):
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    sql.execute(f"INSERT INTO users (user_id, name, phone_number, reg_date) "
                f"VALUES (?, ?, ?, ?);", (user_id, name, phone_number, datetime.now()))
    connection.commit()

def check_user(user_id):
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    checker = sql.execute("SELECT * FROM users WHERE user_id=?;", (user_id, )).fetchone()
    if checker:
        return True
    elif not checker:
        return False

def get_all_users():
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    all_users = sql.execute("SELECT * FROM users;").fetchall()
    return all_users

# взаимодействие с продуктами
def add_product(pr_name, pr_price, pr_desc, pr_quantity, pr_photo):
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    sql.execute("INSERT INTO products (pr_name, pr_price, pr_desc, "
                "pr_quantity, pr_photo, reg_date) "
                "VALUES (?, ?, ?, ?, ?, ?);", (pr_name, pr_price, pr_desc,
                                              pr_quantity, pr_photo,
                                              datetime.now()))
    connection.commit()
def get_all_products():
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    all_product = sql.execute("SELECT * FROM products;").fetchall()
    return all_product
def delete_exact_product(pr_id):
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    sql.execute("DELETE FROM products WHERE pr_id = ?;", (pr_id, ))
    connection.commit()
# дз функция изменения количества определенного продукта
def change_quantity(something):
        pass

def delete_all_products():
    connection = sqlite3.connect("data.db")
    sql = connection.cursor()
    sql.execute("DELETE FROM products;")
    connection.commit()




