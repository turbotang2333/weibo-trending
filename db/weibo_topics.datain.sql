BEGIN TRANSACTION;
-- 遍历all_topics表中的每一行数据
INSERT INTO topics (topic)
SELECT DISTINCT topic
FROM all_topics;
INSERT INTO dates (date)
SELECT DISTINCT date
FROM all_topics;
INSERT INTO topic_date (topic_id, date_id)
SELECT topics.id,
    dates.id
FROM all_topics
    INNER JOIN topics ON all_topics.topic = topics.topic
    INNER JOIN dates ON all_topics.date = dates.date;
COMMIT;