import databases
import sqlalchemy

from iot_device_api.config import config

# stores information about our database
metadata = sqlalchemy.MetaData()


device_table = sqlalchemy.Table(
    "devices",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("locationType", sqlalchemy.String),
    sqlalchemy.Column("category", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.String),
    sqlalchemy.Column("latitude", sqlalchemy.Integer),
    sqlalchemy.Column("longitude", sqlalchemy.Integer),
    sqlalchemy.Column("createTime", sqlalchemy.DateTime),
    sqlalchemy.Column("updateTime", sqlalchemy.DateTime)
)


engine = sqlalchemy.create_engine(
    config.DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK
)