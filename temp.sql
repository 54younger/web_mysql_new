DROP DATABASE IF EXISTS test_temp;
CREATE DATABASE test_temp;
USE test_temp;

CREATE TABLE user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE topic (
    topic_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE post (
    post_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    topic_id INT NOT NULL,
    user_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT post_ibfk_1 FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    CONSTRAINT post_ibfk_2 FOREIGN KEY (topic_id) REFERENCES topic(topic_id) ON DELETE CASCADE
);

CREATE TABLE comment (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    user_id INT NOT NULL,
    post_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT comment_ibfk_1 FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    CONSTRAINT comment_ibfk_2 FOREIGN KEY (post_id) REFERENCES post(post_id) ON DELETE CASCADE
);


-- 插入用户数据
INSERT INTO user (username, email, password)
VALUES ('John', 'john@example.com', 'password123'),
       ('Jane', 'jane@example.com', 'password456'),
       ('Bob', 'bob@example.com', 'password789');

-- 插入话题数据
INSERT INTO topic (name, description)
VALUES ('Technology', 'Discussions about technology.'),
       ('Sports', 'Discussions about sports.'),
       ('Politics', 'Discussions about politics.');


-- 插入文章数据
INSERT INTO post (title, content, topic_id, user_id)
VALUES ('First Post', 'This is my first post.', 1, 1),
       ('Second Post', 'This is my second post.', 2, 2),
       ('Third Post', 'This is my third post.', 2, 3);

-- 插入评论数据
INSERT INTO comment (content, user_id, post_id)
VALUES ('Great post!', 2, 1),
       ('Thanks for sharing!', 3, 1),
       ('I really enjoyed reading this.', 1, 2),
       ('Can''t wait for your next post!', 2, 2),
       ('Interesting perspective.', 3, 3);



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
