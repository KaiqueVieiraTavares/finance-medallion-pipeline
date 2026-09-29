import os
from dataclasses import dataclass
from datetime import datetime

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Config:
    # AWS / S3
    aws_region: str
    s3_bucket_name: str
    s3_bronze_prefix: str
    s3_silver_prefix: str
    s3_gold_prefix: str

    # GCP / BigQuery
    gcp_project_id: str
    bigquery_dataset: str
    bigquery_daily_table: str
    bigquery_risk_table: str
    google_credentials_path: str

    # Pipeline
    processing_date: str | None
    log_level: str


def get_required_env(variable_name: str) -> str:
    value = os.getenv(variable_name)

    if not value:
        raise ValueError(
            f"A variável de ambiente obrigatória "
            f"'{variable_name}' não foi definida."
        )

    return value


def validate_processing_date(date_value: str | None) -> str | None:
    if date_value is None:
        return None

    try:
        datetime.strptime(date_value, "%Y-%m-%d")
    except ValueError as error:
        raise ValueError(
            "PROCESSING_DATE deve estar no formato YYYY-MM-DD."
        ) from error

    return date_value


def load_config() -> Config:
    return Config(
        aws_region=get_required_env("AWS_REGION"),
        s3_bucket_name=get_required_env("S3_BUCKET_NAME"),
        s3_bronze_prefix=os.getenv("S3_BRONZE_PREFIX", "bronze"),
        s3_silver_prefix=os.getenv("S3_SILVER_PREFIX", "silver"),
        s3_gold_prefix=os.getenv("S3_GOLD_PREFIX", "gold"),

        gcp_project_id=get_required_env("GCP_PROJECT_ID"),
        bigquery_dataset=os.getenv(
            "BIGQUERY_DATASET",
            "finance_analytics",
        ),
        bigquery_daily_table=os.getenv(
            "BIGQUERY_DAILY_TABLE",
            "gold_daily_asset_metrics",
        ),
        bigquery_risk_table=os.getenv(
            "BIGQUERY_RISK_TABLE",
            "gold_rolling_risk_metrics",
        ),
        google_credentials_path=get_required_env(
            "GOOGLE_APPLICATION_CREDENTIALS"
        ),

        processing_date=validate_processing_date(
            os.getenv("PROCESSING_DATE")
        ),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )