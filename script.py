import logging
from typing import Any, Dict, List, Optional, Union
import credentials
import praw

# Credentials to use PRAW to fetch data
reddit = praw.Reddit(
    client_id=credentials.CLIENT_ID,
    client_secret=credentials.CLIENT_SECRET,
    password=credentials.PASSWORD,
    user_agent=credentials.USER_AGENT,
    username=credentials.USER_NAME
)


def get_hot_posts(subreddit: Any) -> List[List[str]]:
    """
    Function to get hot posts of the given subreddit
    Args:
        subreddit: Stores the subreddit of the given string
    Returns(List):
        URLs and titles of the posts of the given subreddit
    """
    try:
        hot_posts: Any = subreddit.hot(limit=5)
    except Exception as e:
        logging.exception("Posts cannot be fetched" + str(e))
        pass
    titles: List[str] = []
    urls: List[str] = []
    for post in hot_posts:
        urls.append(post)
        titles.append(post.title)
    return [urls, titles]


def get_comments(url: str) -> Dict[Optional[str], str]:
    """
    Function to get top comments of a post
    Args:
        url(str): Stores the URL of a post
    Returns(dict):
        Dictionary which consists name of author and its comment
    """
    try:
        submission: Any = reddit.submission(str(url))
        comments: Dict[Optional[str], str] = dict()
        for top_comment in submission.comments:
            try:
                comments[get_author(top_comment.id)] = top_comment.body
            except Exception as e:
                logging.exception("top_comment does not exist" + str(e))
                pass
    except Exception as e:
        logging.exception("url is invalid" + str(e))
        pass
    return comments


def get_author(comment_id: str) -> Union[str, None]:
    """
    Function to get name of author of a comment
    Args:
        comment_id(str): Stores the id of the comment
    Returns(str):
        name of the author of the comment
    """
    comment: Any = reddit.comment(comment_id)
    try:
        author: Any = comment.author
        if author and author.name:
            return author.name
        return None
    except Exception as e:
        logging.exception("Comment is removed by the author" + str(e))
        pass
    return None


if __name__ == "__main__":
    subreddit_input: str = input("Enter any subreddit: ")
    subreddit: Any = reddit.subreddit(subreddit_input)
    [urls, titles] = get_hot_posts(subreddit)

    for url, title in zip(urls, titles):
        comments: Dict[Optional[str], str] = get_comments(url)
        print("========================================================")
        print(f"Title: {title}\n")
        print("Comments:\n")
        for key, value in comments.items():
            print(f"Name: {key}\nComment: {value}\n")
