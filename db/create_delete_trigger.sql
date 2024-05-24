-- 创建删除触发器
CREATE TRIGGER after_delete_all_topics
AFTER DELETE ON all_topics FOR EACH ROW BEGIN -- 删除 topic_date 表中对应的记录
DELETE FROM topic_date
WHERE topic_id = (
        SELECT id
        FROM topics
        WHERE topic = OLD.topic
    )
    AND date_id = (
        SELECT id
        FROM dates
        WHERE date = OLD.date
    );
-- 删除未被引用的 topic
DELETE FROM topics
WHERE id = (
        SELECT id
        FROM topics
        WHERE topic = OLD.topic
    )
    AND NOT EXISTS (
        SELECT 1
        FROM all_topics
        WHERE topic = OLD.topic
    );
-- 删除未被引用的 date
DELETE FROM dates
WHERE id = (
        SELECT id
        FROM dates
        WHERE date = OLD.date
    )
    AND NOT EXISTS (
        SELECT 1
        FROM all_topics
        WHERE date = OLD.date
    );
END;