CREATE DATABASE IF NOT EXISTS reddit_comments;

USE reddit_comments;

CREATE TABLE Author (
  author varchar(255) PRIMARY KEY,
  author_fullname varchar(255),
  author_created_utc TIMESTAMP NULL
  -- author_flair_css_class varchar(255),
  -- author_flair_text varchar(255)
);

CREATE TABLE Subreddit (
  id varchar(255) PRIMARY KEY,
  subreddit_name varchar(255),
  subreddit_name_prefixed varchar(255),
  subreddit_type varchar(255)
);


SET SQL_MODE='ALLOW_INVALID_DATES';

CREATE TABLE Comment (
  id varchar(255) PRIMARY KEY,
  link_id varchar(255),
  parent_id varchar(255),
  subreddit_id varchar(255),
  author varchar(255),
  score int,
  gilded int,
  ups int,
  downs int,
  controversiality int,
  created_utc TIMESTAMP  NULL,
  retrieved_on TIMESTAMP NULL,
  permalink varchar(255)
);

CREATE TABLE CommentDetail (
  id varchar(255) PRIMARY KEY,
  name varchar(255),
  body text,
  archived boolean,
  edited boolean,
  stickied boolean,
  distinguished text,
  removal_reason text,
  score_hidden boolean
);

ALTER TABLE CommentDetail ADD FOREIGN KEY (id) REFERENCES Comment (id);

ALTER TABLE Comment ADD FOREIGN KEY (subreddit_id) REFERENCES Subreddit (id);

ALTER TABLE Comment ADD FOREIGN KEY (author) REFERENCES Author (author);