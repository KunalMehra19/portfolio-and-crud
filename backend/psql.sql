-- Drop tables if they exist
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS blogs;

-- Create blogs table
CREATE TABLE blogs (
  blog_id TEXT PRIMARY KEY NOT NULL,
  blog_title TEXT NOT NULL,
  blog_content TEXT NOT NULL,
  blog_author TEXT NOT NULL,
  blog_timestamps TIMESTAMP CURRENT_TIMESTAMP
);

-- Create users table
CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  contact BIGINT UNIQUE NOT NULL,
  pwd TEXT NOT NULL
);

-- Create comments table
CREATE TABLE comments (
  comment_id TEXT PRIMARY KEY NOT NULL,
  comment_title TEXT NOT NULL,
  comment_content TEXT NOT NULL,
  comment_author TEXT NOT NULL,
  comment_timestamps TIMESTAMP CURRENT_TIMESTAMP
);