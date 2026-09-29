import pyspark.sql.types as t
from pyspark.sql import SparkSession, DataFrame

BRONZE_COLUMNS = [
"open_time",
"open",
"high",
"low",
"close",
"volume",
"close_time",
"quote_asset_volume",
"number_of_trades",
"taker_buy_base_asset_volume",
"taker_buy_quote_asset_volume",
"ignore",
]

def get_bronze_schema(colunas: list[str]) -> t.StructType:
    fields_list: list[t.StructField] = []
    for col in colunas:
        fields_list.append(t.StructField(col, t.StringType(), nullable=True))

    return t.StructType(fields_list)


def read_bronze_data(session: SparkSession, path: str, schema: t.StructType) -> DataFrame:
    return session.read.schema(schema).csv(path)