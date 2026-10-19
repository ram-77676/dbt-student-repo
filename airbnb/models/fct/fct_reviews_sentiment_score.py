
from textblob import TextBlob
import snowflake.snowpark.functions as F
import snowflake.snowpark.types as T


def model(dbt, session):
    dbt.config(
        materialized="table",
        packages=["textblob"]
    )

    # Read the existing reviews model
    reviews_df = dbt.ref("fct_reviews")

    # Register the UDF using a lambda function
    sentiment_udf = F.udf(
        lambda text: (
            0.0 if text is None
            else float(TextBlob(text).sentiment.polarity)
        ),
        return_type=T.FloatType(),
        input_types=[T.StringType()],
        packages=["textblob"]
    )

    # Add sentiment polarity to each review
    result_df = reviews_df.with_column(
        "SENTIMENT_SCORE",
        sentiment_udf(F.col("REVIEW_TEXT"))
    )

    return result_df
