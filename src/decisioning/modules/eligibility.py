import polars as pl


def check_eligibility(df: pl.DataFrame) -> pl.DataFrame:
    # D1001: Check if age is 18 or older
    df = df.with_columns(
        pl.when(pl.col("age") >= 18)
        .then(pl.lit("Y"))
        .otherwise(pl.lit("N"))
        .alias("D1001_eligible")
    )
