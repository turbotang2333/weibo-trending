-- 创建触发器
CREATE TRIGGER after_insert_all_topics
AFTER
INSERT ON all_topics FOR EACH ROW BEGIN -- 插入新的话题到 topics 表，如果已经存在则忽略
INSERT
    OR IGNORE INTO topics (topic)
VALUES (NEW.topic);
-- 插入新的日期到 dates 表，如果已经存在则忽略
INSERT
    OR IGNORE INTO dates (date)
VALUES (NEW.date);
-- 获取 topic_id 和 date_id 并插入到 topic_date 表，如果组合已经存在则忽略
INSERT
    OR IGNORE INTO topic_date (topic_id, date_id)
VALUES (
        (
            SELECT id
            FROM topics
            WHERE topic = NEW.topic
        ),
        (
            SELECT id
            FROM dates
            WHERE date = NEW.date
        )
    );
END;