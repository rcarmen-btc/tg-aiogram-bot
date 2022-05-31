from avia_api import AviasalesAPI
from pprint import pp, pprint
import requests
from sqlalchemy import create_engine
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean
from datetime import datetime

avia = AviasalesAPI('5550916455:AAEGRMaQfYqpNgKOLKIMrdodQW63aVC-2fM', 'ru')

print(len(avia.get_countries()))

# connection = psycopg2.connect(user="postgres", password="postgres", host="db")
# connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#
# cursor = connection.cursor()
# sql_create_database = cursor.execute('create database sqlalchemy_tuts')
#
# cursor.close()
# connection.close()
#
# engine = create_engine("postgresql+psycopg2://postgres:postgres@db/sqlalchemy_tuts")
# engine.connect()
#
# print(engine)



