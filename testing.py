import praw
import credentials
from script import get_comments, get_hot_posts

reddit = praw.Reddit(
    client_id=credentials.CLIENT_ID,
    client_secret=credentials.CLIENT_SECRET,
    password=credentials.PASSWORD,
    user_agent=credentials.USER_AGENT,
    username=credentials.USER_NAME
)


def test_get_hot_posts():
    """
    Test for get_hot_posts function
    """
    input_string = "beauty"
    subreddit = reddit.subreddit(input_string)
    result = get_hot_posts(subreddit)
    assert len(result) == 2
    assert len(result[0]) == len(result[1])
    assert len(result[0]) == 5
    assert type(result) == list


def test_get_comments():
    """
    Test for get_comments function
    """
    input_string = "beauty"
    subreddit = reddit.subreddit(input_string)
    result = get_hot_posts(subreddit)
    comments = get_comments(result[0][0])
    assert len(comments) > 0
    assert type(comments) == dict


def test_get_author():
    """
    Test for get_author function
    """
    input_string = "beauty"
    subreddit = reddit.subreddit(input_string)
    result = get_hot_posts(subreddit)
    submission = reddit.submission(result[0][2])
    assert hasattr(submission, "comments")
    assert hasattr(submission.comments[0], "body")
    comment = reddit.comment(submission.comments[0].id)
    assert hasattr(comment, "author")
