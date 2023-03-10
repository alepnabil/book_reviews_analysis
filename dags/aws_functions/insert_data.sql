INSERT INTO review_fact_table 
(	
	book_author,
	book_name,
    name,
    review,
    ratings_given_out_of_5,
    review_likes,
    review_comments,
    language,
    neg,
    neu,
    pos,
    compound,
    sentiment)
SELECT  
	book_author,
	book_name,
    name,
    review,
    ratings_given_out_of_5,
    review_likes,
    review_comments,
    language,
    neg,
    neu,
    pos,
    compound,
    sentiment
FROM main_table;


INSERT INTO reviewer_dim_table 
(
	name,
    author,
	num_author_books,
    num_author_followers,
    reviewer_reviews,
    reviewer_followers
)
SELECT
	name,
    author,
	num_author_books,
    num_author_followers,
    reviewer_reviews,
    reviewer_followers
FROM main_table;


INSERT INTO book_dim_table 
(
	book_author, 
	book_name, 
	book_theme
)
SELECT book_author, book_name,
       CASE
           WHEN book_name = 'Politik untuk pemula' THEN 'intro'
           WHEN book_name = 'Leviathan' THEN 'social contract'
           -- add more cases as needed
           ELSE 'unknown'
       END AS book_theme
FROM main_table;