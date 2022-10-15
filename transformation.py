def get_num_author_books(author):
    num_author_books=author.split('Author')[1].split('book')[0]
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
