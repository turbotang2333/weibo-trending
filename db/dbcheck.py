import sqlite3

def print_table_structure(db_name):
    # 连接数据库
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # 获取所有表的名字
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # 对于每个表，打印表的结构
    for table_name in tables:
        print(f"Table: {table_name[0]}")
        cursor.execute(f"PRAGMA table_info({table_name[0]});")
        print("Column Info: ID, Name, Type, NotNull, DefaultVal, PrimaryKey")
        for row in cursor.fetchall():
            print(row)

    # 关闭数据库连接
    conn.close()

# 打印weibo_topics.db中的数据表结构
print_table_structure('weibo_topics.db')