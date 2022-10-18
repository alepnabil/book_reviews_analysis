def get_num_author_books(author):
    num_author_books = author.split('Author')[1].split('book')[0]
    return num_author_books


def get_num_author_followers(author):
    author = author.replace('followers', 'follower')

    if 'books' in author:
        num_author_followers = author.split('books')[-1].replace('follower', '')
    elif 'book':
        num_author_followers = author.split('book')[-1].replace('follower', '')

    return num_author_followers


def get_num_reviewer_reviews(reviewer):
    reviews = reviewer.lower()
    reviews = reviewer.replace('reviews', 'review')

    reviews = reviewer.split()[0]

    return reviews


def get_num_reviewer_followers(reviewer):
    if 'follower' in reviewer:
        followers = reviewer.split()[-2]
    elif 'followers' in reviewer:
        followers = reviewer.split()[-2]
    else:
        followers = None

    return followers


def get_ratings(rating):
    rating = rating.split()[1]
    return rating


def get_num_review_likes(review):
    review = review.split()[0]

    return review


def get_num_review_comments(comment):
    comment = comment.split()
    comment_len = len(comment)
    if comment_len >= 4:
        comment = comment[-2]
    else:
        comment = None
    return comment


def get_review_likes(review):
    # Case 1:138 likes 4 comments
    # Case 2:165 likes
    # Case 3:3 comments

    # convert all reviews which has 'likes' to 'like'
    if 'likes' in review:
        review = review.replace('likes', 'like')
    else:
        pass

    review = review.split()
    if 'like' in review:
        review = review[0]
    else:
        review = None

    return review


def get_review_comments(comment):
    # Case 1:138 likes 4 comments
    # Case 2:3 comments
    # Case 3:1 likes

    # convert all reviews which have 'comments' to 'comment'
    if 'comments' in comment:
        comment = comment.replace('comments', 'comment')
    else:
        pass

    # to handle different kind of cases
    review_len = len(comment.split())
    if review_len == 4:
        comment = comment.split()[2]
    elif review_len == 2 and 'comment' in comment:
        comment = comment.split()[0]
    else:
        comment = None

    return comment
