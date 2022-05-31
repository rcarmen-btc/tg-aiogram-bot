from aviasales_api.avia_api import AviasalesAPI
from sqlalchemy import create_engine
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2
from tgbot.config import load_config


def create_db():
    connection = psycopg2.connect(user="postgres", password="postgres", host="db")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = connection.cursor()
    sql_create_database = cursor.execute(f'create database {load_config().db.database}')

    cursor.close()
    connection.close()


def create_tables(engine):
    pass


def load_countries():
    avi = AviasalesAPI(load_config().tg_bot.token, load_config().tg_bot.locale)
    avi.get_countries()

    create_db()

    engine = create_engine("postgresql+psycopg2://postgres:postgres@db/sqlalchemy_tuts")
    engine.connect()

    create_tables(engine)


    print(engine)
