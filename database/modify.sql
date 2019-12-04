USE reddit_comments;

-- create index
CREATE UNIQUE INDEX commentid ON Comment(id);
ALTER TABLE `Comment` ADD INDEX `comment_idx_parent_id` (`parent_id`);
CREATE UNIQUE INDEX id_parent_id ON Comment (id, parent_id);

CREATE UNIQUE INDEX commentdetailid ON CommentDetail(id);
CREATE UNIQUE INDEX commentdetailname ON CommentDetail(name);

CREATE UNIQUE INDEX authorid ON Author(author);
CREATE UNIQUE INDEX subredditid ON Subreddit(id);


-- ********** DEPRECATED **********

-- UPDATE Comment INNER JOIN CommentDetail ON Comment.id = CommentDetail.id SET Comment.body = CommentDetail.body;
-- UPDATE Comment, CommentDetail set Comment.body = CommentDetail.body where Comment.id = CommentDetail.id;