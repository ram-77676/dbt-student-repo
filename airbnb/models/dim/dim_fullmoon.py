
import holidays
from snowflake.snowpark.functions import col, lit, when

def model(dbt, session):
    dbt.config(
        materialized="table",
        packages=["holidays"],
        enabled=False
    )

    orders_df = dbt.ref("seed_full_moon_dates")

    german_holidays = holidays.Germany()
    holiday_dates = [
        str(date)
        for date in german_holidays.keys()
    ]

    return orders_df.with_column(
        "IS_HOLIDAY",
        when(
            col("FULL_MOON_DATE").cast("DATE").isin(holiday_dates),
            lit(True)
        ).otherwise(lit(False))
    )
