import os
import re
import sqlite3
from sqlite3 import Error
import sys

# 创建数据库连接
def create_connection():
    conn = None;
    try:
        print("正在创建数据库连接...")
        conn = sqlite3.connect('weibo_topics.db') # 创建一个在磁盘上的数据库
        print("数据库连接已创建。")
        return conn
    except Error as e:
        print("错误！无法创建数据库连接。")

# 向all_topics数据表中添加话题
def add_topic(conn, topic, date):
    # 插入话题和日期到all_topics表
    sql = ''' INSERT INTO all_topics(topic,date)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (topic, date))
    conn.commit()  # 提交事务
    return cur.lastrowid

# 处理单个.md文件
def process_md_file(database, filename):
    try:
        safe_filename = os.path.basename(filename)
        # 打开并读取文件
        with open(os.path.join('archives', safe_filename), 'r') as f:
            content = f.read()
            # 使用正则表达式找到所有的话题
            topics = re.findall(r'\[([^\]]+)\]', content)
            # 记录每个话题出现的次数
            topic_counts = {}
            for topic in topics:
                if topic in topic_counts:
                    topic_counts[topic] += 1
                else:
                    topic_counts[topic] = 1
            # 打印出重复的话题
            duplicate_topics = [topic for topic, count in topic_counts.items() if count > 1]
            if duplicate_topics:
                print(f"文件 {safe_filename} 中有重复的话题：{', '.join(duplicate_topics)}")
            else:
                print("没有重复的话题")
            # 将找到的话题和文件名（日期）添加到数据库中
            topic_count = 0
            for topic in set(topics):  # 使用set去重
                add_topic(database, topic, safe_filename.replace('.md', ''))
                topic_count += 1
            # 使用\r字符覆盖终端中的内容
            print(f"\r正在处理文件 {safe_filename}，已获取 {topic_count} 个话题", end='')
            if duplicate_topics:
                print("\n已排重")
            print("\n")
            sys.stdout.flush()  # 手动刷新输出缓冲区
    except Error as e:
        print(f"\r错误！无法处理文件 {safe_filename}，错误信息：{e}")
        sys.stdout.flush()  # 手动刷新输出缓冲区

# 删除导入的错误日期数据
def delete_wrong_data(conn, wrong_date):
    sql = ''' DELETE FROM all_topics WHERE date = ? '''
    cur = conn.cursor()
    cur.execute(sql, (wrong_date,))
    conn.commit()

##################################################
# 以下是运行主函数
##################################################

def main():
    # 创建数据库连接
    database = create_connection()

    # 获取用户的选择
    print("请选择要执行的操作：")
    print("1. 按日期添加话题")
    print("2. 按日期删除话题")
    choice = input("请输入你的选择（1或2）：")

    # 获取日期
    date = input("请输入日期（格式：YYYY-MM-DD）：")

    if choice == '1':
        # 处理指定的.md文件
        filename = f"archives/{date}.md"
        print(f"正在处理文件 {filename}...")
        process_md_file(database, filename)
    elif choice == '2':
        # 删除错误数据
        print(f"正在删除日期为 {date} 的数据...")
        delete_wrong_data(database, date)
    else:
        print("无效的选择。请重新运行脚本并输入1或2。")

if __name__ == '__main__':
    main()
