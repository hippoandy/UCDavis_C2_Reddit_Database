-- SELECT count(*) as count, subreddit 
-- FROM [fh-bigquery:reddit_posts.2015_12] 
-- GROUP BY subreddit 
-- ORDER BY count DESC;

SELECT count(*) as count, subreddit_id
FROM Comment
GROUP BY subreddit_id
ORDER BY count DESC;

-- SELECT Parent.id, Parent.body, comment.author, comment.parent_id, comment.body
-- FROM Parent
-- LEFT JOIN comment ON comment.parent_id = Parent.id;

-- 9 min 49.06 sec
SELECT Comment.id, Comment.parent_id, CommentDetail.body
    INTO OUTFILE '/tmp/test.csv'
    FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
FROM Comment, CommentDetail
WHERE Comment.parent_id LIKE 't1_%' AND Comment.id = CommentDetail.id
;

-- 6 min 41.72 sec
SELECT CONCAT( "t1_", Comment.id ) AS parent_id, Comment.id AS id, CommentDetail.body
    INTO OUTFILE '/tmp/test.csv'
    FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
FROM Comment
LEFT JOIN CommentDetail ON Comment.id = CommentDetail.id
WHERE Comment.parent_id LIKE 't1_%'
;

-- 28 min 44.58 sec, 57530398 rows
-- child
SELECT Comment.id, Comment.author, CommentDetail.body AS child_body, Parent.name AS parent_id, Parent.body AS parent_body
    INTO OUTFILE '/tmp/test.csv'
    FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
FROM Comment
LEFT JOIN CommentDetail
-- only find the comment where parent is a comment as well
ON Comment.parent_id LIKE 't1_%' AND Comment.id = CommentDetail.id
-- parent
INNER JOIN (
    SELECT CommentDetail.name, CommentDetail.body
    FROM CommentDetail
) AS Parent ON Comment.parent_id = Parent.name
;

-- 32 min 1.88 sec, 57530398 rows
-- child
SELECT
    Parent.name AS parent_id,
    -- replace nextline char with space
    REPLACE( REPLACE( Parent.body, char(10), char(32) ), char(13), char(32) ) AS parent_body,
    Comment.id,
    Comment.author,
    REPLACE( REPLACE( CommentDetail.body, char(10), char(32) ), char(13), char(32) ) AS child_body
INTO OUTFILE '/tmp/test.csv'
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
FROM Comment
LEFT JOIN CommentDetail
-- only find the comment where parent is a comment as well
ON Comment.parent_id LIKE 't1_%' AND Comment.id = CommentDetail.id
-- parent
INNER JOIN (
    SELECT CommentDetail.name, CommentDetail.body
    FROM CommentDetail
-- make sure the parent is not itself
) AS Parent ON CONCAT( "t1_", Comment.id ) <> Comment.parent_id AND Comment.parent_id = Parent.name
;