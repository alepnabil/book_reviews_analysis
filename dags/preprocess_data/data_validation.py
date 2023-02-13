import pandas as pd
import pandera as pa
from pandera.errors import SchemaErrors
from pandera import Column, Check, DataFrameSchema


def check_num_columns(df):
    if df.shape[1] == 14:
        pass
    else:
        return "Invalid number of columns"


def column_type_validation(df):
    try:
        schema = DataFrameSchema({
            "name": Column(object),
            "review": Column(object),
            "author": Column(bool),
            "num_author_books": Column(pa.dtypes.Int32, required=False, nullable=True),
            "num_author_followers": Column(pa.dtypes.Int32, required=False, nullable=True),
            "reviewer_reviews": Column(pa.dtypes.Int32, required=False, nullable=True),
            "reviewer_followers": Column(pa.dtypes.Int32, required=False, nullable=True),
            "ratings_given_out_of_5": Column(pa.dtypes.Int8, nullable=True),
            "review_likes": Column(pa.dtypes.Int32, required=False, nullable=True),
            "review_comments": Column(pa.dtypes.Int32, required=False, nullable=True),
            "language": Column(object),
            "clean_review": Column(object),
            "sentiment_score": Column(float),
            "sentiment": Column(object)
        })
        validated_df = schema.validate(df)
    except SchemaErrors as err:
        return err.failure_cases


def column_check_validation(df):
    try:
        schema = DataFrameSchema({
            "num_author_books": Column(pa.dtypes.Int32, Check.greater_than_or_equal_to(0), nullable=True),
            "num_author_followers": Column(pa.dtypes.Int32, Check.greater_than_or_equal_to(0), nullable=True),
            "reviewer_reviews": Column(pa.dtypes.Int32, Check.greater_than_or_equal_to(0), nullable=True),
            "reviewer_followers": Column(pa.dtypes.Int32, Check.greater_than_or_equal_to(0), nullable=True),
            "ratings_given_out_of_5": Column(pa.dtypes.Int8, Check.in_range(0, 5), nullable=True),
            "review_likes": Column(pa.dtypes.Int32, Check.greater_than_or_equal_to(0), nullable=True),
            "reviewer_followers": Column(pa.dtypes.Int32, Check.greater_than_or_equal_to(0), nullable=True),
            "review_comments": Column(pa.dtypes.Int32, Check.greater_than_or_equal_to(0), nullable=True),
            "sentiment_score": Column(pa.dtypes.Float64, Check.in_range(-1, 1), nullable=True),
        })
        schema.validate(df)
    except SchemaErrors as err:
        return err.failure_cases

