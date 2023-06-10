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
