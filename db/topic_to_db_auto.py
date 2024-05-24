# -*- coding: utf-8 -*-

import os
import re
import sqlite3
from sqlite3 import Error
import sys
import glob

# 连接数据库
def create_connection():
    conn = None
    try:
        print("Connecting to the database...")
        conn = sqlite3.connect('weibo_topics.db')
        print("Connection successful")
        return conn
    except Error as e:
        print(f"Error connecting to the database: {e}")

# 添加话题到数据库
def add_topic(conn, topic, date):
    sql = ''' INSERT INTO all_topics(topic, date) VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (topic, date))
    conn.commit()
    return cur.lastrowid

# 处理 .md 文件
def process_md_file(database, filename):
    try:
        safe_filename = os.path.basename(filename)
        with open(os.path.join('archives', safe_filename), 'r') as f:
            content = f.read()
            topics = re.findall(r'\[([^\]]+)\]', content)
            topic_counts = {}
            for topic in topics:
                if topic in topic_counts:
                    topic_counts[topic] += 1
                else:
                    topic_counts[topic] = 1
            duplicate_topics = [topic for topic, count in topic_counts.items() if count > 1]
            if duplicate_topics:
                print(f"Duplicates found in {safe_filename}: {', '.join(duplicate_topics)}")
            else:
                print("No duplicates found")
            topic_count = 0
            for topic in set(topics):
                add_topic(database, topic, safe_filename.replace('.md', ''))
                topic_count += 1
            print(f"Processed {safe_filename} with {topic_count} topics")
        sys.stdout.flush()
    except Error as e:
        print(f"Error processing {safe_filename}: {e}")
        sys.stdout.flush()

# 删除错误日期的数据
def delete_wrong_data(conn, wrong_date):
    sql = ''' DELETE FROM all_topics WHERE date = ? '''
    cur = conn.cursor()
    cur.execute(sql, (wrong_date,))
    conn.commit()

# 查找最新的 .md 文件
def find_latest_md_file():
    md_files = glob.glob('archives/*.md')
    if not md_files:
        return None
    latest_file = max(md_files, key=os.path.getmtime)
    return latest_file

# 主函数
def main():
    database = create_connection()
    latest_file = find_latest_md_file()

    if latest_file:
        print(f"Processing latest file: {latest_file}")
        process_md_file(database, latest_file)
    else:
        print("No .md files found in the archives folder")

if __name__ == "__main__":
    main()
