import os
import re
from collections import Counter
import sqlite3
from glob import glob

def process_md_file(file_path):
    # 如果文件不是md文件，直接返回
    if not file_path.endswith('.md'):
        return

    # 打开文件
    with open(file_path, 'r') as file:
        content = file.read()

    # 提取日期
    date = os.path.basename(file.name).split('.')[0]

    # 提取话题
    topics = re.findall(r'\[(.*?)\]', content)

    # 计算每个话题的出现次数
    topic_counts = Counter(topics)

    # 找出出现次数大于1的话题
    duplicate_topics = {topic: count for topic, count in topic_counts.items() if count > 1}

    # 如果有重复的话题，只打印有多少个重复的话题
    if duplicate_topics:
        print(f"有{len(duplicate_topics)}个重复的话题")
        # 排除重复的话题
        unique_topics = list(set(topics))
        # 打印排重完成
        print("排重完成")
    # 如果没有重复的话题，打印"没有重复话题"
    else:
        print("没有重复话题")
        unique_topics = topics

    # 将数据插入all_topics表
    for topic in unique_topics:
        cursor.execute('INSERT INTO all_topics (topic, date) VALUES (?, ?)', (topic, date))

    # 提交事务
    conn.commit()

# 使用上下文管理器处理数据库连接和游标
with sqlite3.connect('weibo_topics.db') as conn:
    cursor = conn.cursor()

    # 创建all_topics表
    cursor.execute('CREATE TABLE IF NOT EXISTS all_topics (topic TEXT, date TEXT)')

    # 获取archives目录下的所有md文件
    files = glob('archives/*.md')

    # 按文件名排序，从早到晚处理文件
    files.sort()

    # 遍历所有文件
    for file in files:
        # 打印正在处理的文件名
        print(f"正在处理{file}文件")
        # 调用process_md_file函数处理文件
        process_md_file(file)