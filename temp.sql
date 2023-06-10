
-- 单表查询存储过程
DELIMITER //
CREATE PROCEDURE GetPostsByTopic(IN topic_id INT)
BEGIN
    SELECT p.*
    FROM post p
    WHERE p.topic_id = topic_id;
END //
DELIMITER ;

-- 数据插入存储过程
DELIMITER //
CREATE PROCEDURE CreatePost(
    IN p_title VARCHAR(100),
    IN p_content TEXT,
    IN p_topic_id INT,
    IN p_user_id INT
)
BEGIN
    INSERT INTO post (title, content, topic_id, user_id)
    VALUES (p_title, p_content, p_topic_id, p_user_id);
END //
DELIMITER ;



-- 数据删除存储过程
DELIMITER //
CREATE PROCEDURE DeletePost(IN p_post_id INT)
BEGIN
    DELETE FROM post WHERE post_id = p_post_id;
    DELETE FROM comment WHERE post_id = p_post_id;
END //
DELIMITER ;


-- 数据修改存储过程
DELIMITER //
CREATE PROCEDURE UpdatePost(
    IN p_post_id INT,
    IN p_content TEXT
)
BEGIN
    UPDATE post
    SET content = p_content
    WHERE post_id = p_post_id;
END //
DELIMITER ;

-- 测试
CALL GetPostsByTopic(1);
SELECT * FROM post;
CALL CreatePost('New Post', 'This is a new post content.', 2, 1);
SELECT * FROM post;
CALL UpdatePost(2, 'This is the updated content.');
SELECT * FROM post;
CALL DeletePost(3);
SELECT * FROM post;

-- 创建日志表log
CREATE TABLE log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    operation VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建数据插入触发器
DELIMITER //
CREATE TRIGGER user_insert_trigger
AFTER INSERT ON user
FOR EACH ROW
BEGIN
    INSERT INTO log (table_name, operation) VALUES ('user', 'insert');
END //
DELIMITER ;

-- 创建数据更新触发器
DELIMITER //
CREATE TRIGGER user_update_trigger
AFTER UPDATE ON user
FOR EACH ROW
BEGIN
    INSERT INTO log (table_name, operation) VALUES ('user', 'update');
END //
DELIMITER ;


-- 创建数据删除触发器
DELIMITER //
CREATE TRIGGER user_delete_trigger
AFTER DELETE ON user
FOR EACH ROW
BEGIN
    INSERT INTO log (table_name, operation) VALUES ('user', 'delete');
END //
DELIMITER ;

-- 插入用户数据
INSERT INTO user (username, email, password)
VALUES ('newone', 'newone@example.com', 'password123');

-- 查看日志表是否记录了插入操作
SELECT * FROM log;


-- 更新用户数据
UPDATE user SET password = 'newpassword' WHERE user_id = 1;

-- 查看日志表是否记录了更新操作
SELECT * FROM log;


-- 删除用户数据
DELETE FROM user WHERE user_id = 1;

-- 查看日志表是否记录了删除操作
SELECT * FROM log;

ALTER TABLE post ADD INDEX (post_id);
