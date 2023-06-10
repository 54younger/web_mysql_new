SHOW master status;
show binlog events in 'binlog.000112';
INSERT INTO user (username, email, password) VALUES ('new', 'new@example.com', 'password123');
show binlog events in 'binlog.000112';


CREATE USER 'user1'@'localhost' IDENTIFIED BY 'password1';
GRANT SELECT ON test_temp.* TO 'user1'@'localhost';

CREATE USER 'user2'@'localhost' IDENTIFIED BY 'password2';
GRANT SELECT, INSERT, UPDATE, DELETE ON test_temp.* TO 'user2'@'localhost';


SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- 查询文章评论
SELECT * FROM comment;

-- 尝试修改评论
UPDATE comment SET content = '修改后的评论1' WHERE comment_id = 4;
UPDATE comment SET content = '修改后的评论2' WHERE comment_id = 4;
