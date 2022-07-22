import logging
from typing import Any, List

import praw

import credentials

# Credentials to use PRAW to fetch data
reddit = praw.Reddit(
    client_id=credentials.CLIENT_ID,
    client_secret=credentials.CLIENT_SECRET,
    password=credentials.PASSWORD,
    user_agent=credentials.USER_AGENT,
    username=credentials.USER_NAME,
)


class Post:
    def __init__(self, title: str):
        self.title = title
        self.comments = []

    def __str__(self):
        ans = f"Title: {self.title}\nComments:"
        for comment in self.comments:
            ans += f" {comment}"
        if not len(self.comments):
            ans += " [none]"
        ans += "\n"
        return ans

    def __repr__(self):
        ans = f"Title: {self.title}\nComments:"
        for comment in self.comments:
            ans += f" {comment}"
        if not len(self.comments):
            ans += " [none]"
        ans += "\n"
        return ans


class Comment:
    def __init__(self, author: str, body: str, depth: int):
        self.author = author
        self.body = body
        self.depth = depth
        self.replies = []

    def __str__(self):
        space = "\t" * self.depth
        ans = f"\n{space}Author: {self.author}\n{space}Comment: {self.body}\n{space}Replies:"
        for reply in self.replies:
            ans += f" {reply}"
        if not len(self.replies):
            ans += " [none]"
        ans += "\n"
        return ans

    def __repr__(self):
        space = "\t" * self.depth
        ans = f"\n{space}Author: {self.author}\n{space}Comment: {self.body}\n{space}Replies:"
        for reply in self.replies:
            ans += f" {reply}"
        ans += "\n"
        return ans


def get_hot_posts(subreddit: Any):
    """
    Function to get hot posts of the given subreddit
    Args:
        subreddit: Stores the subreddit of the given string
    Returns(List):
        URLs and titles of the posts of the given subreddit
    """
    try:
        hot_posts: Any = subreddit.hot(limit=1)
    except Exception as e:
        logging.exception("Posts cannot be fetched" + str(e))
        pass
    titles: List[str] = []
    urls: List[str] = []
    for post in hot_posts:
        urls.append(post)
        titles.append(post.title)
    return [urls, titles]


def get_replies(comment: Comment, depth: int) -> List[Comment]:
    """
    Function to get replies of a comment
    Args:
        comment: Stores the id of the comment
        depth: Stores the depth of reply in comment forest
    Returns(List):
        List of replies of the comment
    """
    replies: List[Comment] = []
    if comment.replies:
        for reply in comment.replies:
            myReply = Comment("", "", 0)
            myReply.body = reply.body.replace("\n", " ").replace("\t", " ")
            myReply.author = reply.author.name if reply.author else "[deleted]"
            myReply.depth = depth
            myReply.replies = get_replies(reply, depth + 1)
            replies.append(myReply)
    return replies


def get_comments(url: str) -> List[Comment]:
    """
    Function to get top comments of a post
    Args:
        url(str): Stores the URL of a post
    Returns(List):
        List which consists name of author, comment and its replies
    """
    comments: List[Comment] = []
    submission: Any = reddit.submission(str(url))
    for comment in submission.comments:
        myComment = Comment("", "", 0)
        myComment.body = comment.body.replace("\n", " ").replace("\t", " ")
        myComment.author = comment.author.name if comment.author else "[deleted]"
        myComment.replies = get_replies(comment, 1)
        comments.append(myComment)
    return comments


if __name__ == "__main__":
    subreddit_input = input("Enter any subreddit: ")
    subreddit = reddit.subreddit(subreddit_input)
    [urls, titles] = get_hot_posts(subreddit)
    posts = []

    for url, title in zip(urls, titles):
        post = Post(title)
        post.comments = get_comments(url)
        posts.append(post)

    print(*posts, sep="\n")
