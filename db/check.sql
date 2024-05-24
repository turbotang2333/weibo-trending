-- INSERT INTO all_topics(topic, date) VALUES ('新话题1', '2024-05-24');
-- INSERT INTO all_topics(topic, date) VALUES ('新话题2', '2024-05-24');
-- SELECT name FROM sqlite_master WHERE type='trigger';
DELETE FROM all_topics
WHERE topic = "新话题1";
-- SELECT name FROM sqlite_master WHERE type='table';
-- DROP TRIGGER IF EXISTS after_insert_all_topics;