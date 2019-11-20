USE reddit_comments;

-- create index
CREATE UNIQUE INDEX commentid ON Comment(id);
CREATE UNIQUE INDEX commentdetailid ON CommentDetail(id);
CREATE UNIQUE INDEX authorid ON Author(author);
CREATE UNIQUE INDEX subredditid ON Subreddit(id);
