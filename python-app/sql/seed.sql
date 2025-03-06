INSERT INTO users (username, email) VALUES
('user1', 'user1@example.com'),
('user2', 'user2@example.com'),
('user3', 'user3@example.com');

INSERT INTO posts (user_id, title, content) VALUES
(1, 'First Post', 'This is the content of the first post.'),
(2, 'Second Post', 'This is the content of the second post.'),
(3, 'Third Post', 'This is the content of the third post.');

INSERT INTO comments (post_id, user_id, comment) VALUES
(1, 2, 'This is a comment on the first post by user2.'),
(2, 3, 'This is a comment on the second post by user3.'),
(3, 1, 'This is a comment on the third post by user1.');
