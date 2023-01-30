import praw
import configparser
import sqlite3
from sqlite3 import Error


config = configparser.ConfigParser()
config.read('conf.ini')
reddit_user = config['REDDIT']['reddit_user']
reddit_pass = config['REDDIT']['reddit_pass']
reddit_client_id = config['REDDIT']['reddit_client_id']
reddit_client_secret = config['REDDIT']['reddit_client_secret']
reddit_target_subreddit = config['REDDIT']['reddit_target_subreddit']
max_reports = int(config['SETTINGS']['max_reports'])
flair_text = config['SETTINGS']['flair_text']
keyword = config['SETTINGS']['keyword']

reddit = praw.Reddit(
    username=reddit_user,
    password=reddit_pass,
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent='Reddit Dead Flairing Thing (by u/impshum)'
)


def db_connect():
    try:
        conn = sqlite3.connect('data.db')
        create_table = """CREATE TABLE IF NOT EXISTS posts (
                                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        submission_id TEXT NOT NULL,
                                        author TEXT NOT NULL
                                        );"""
        conn.execute(create_table)
        create_table = """CREATE TABLE IF NOT EXISTS dead_posts (
                                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                        submission_id TEXT NOT NULL
                                        );"""
        conn.execute(create_table)
        return conn
    except Error as e:
        print(e)
    return None


def insert_row(conn, submission, submission_id, author):
    cur = conn.cursor()

    cur.execute("SELECT * FROM dead_posts WHERE submission_id = ? LIMIT 1", (submission_id,))
    result = cur.fetchone()

    if not result:
        cur.execute("SELECT * FROM posts WHERE submission_id = ? AND author = ? LIMIT 1", (submission_id, author))
        result = cur.fetchone()

        if not result:
            conn.execute("INSERT INTO posts (submission_id, author) VALUES (?, ?);", (submission_id, author))
            conn.commit()

        cur.execute("SELECT COUNT(submission_id) FROM posts WHERE submission_id = ?", (submission_id,))
        result = cur.fetchone()

        if result[0] == max_reports:
            print(f'Flairing...')
            conn.execute("INSERT INTO dead_posts (submission_id) VALUES (?);", (submission_id,))
            conn.commit()

            submission.mod.flair(text=flair_text)


def main():
    conn = db_connect()

    for submission in reddit.subreddit(reddit_target_subreddit).new(limit=None):
        for comment in submission.comments:
            comment_body = comment.body
            if keyword in comment_body:
                insert_row(conn, submission, submission.id, comment.author.name)


if __name__ == '__main__':
    main()
