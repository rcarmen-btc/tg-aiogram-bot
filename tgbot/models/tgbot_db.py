from sqlalchemy import sql, Column, Sequence

from db.tgbot.database import db


class Country(db.Model):
    __tablename__ = 'countries'

    query: sql.Select

    id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    code = db.Column(db.String(10))
    name = db.Column(db.String(100))
    currency = db.Column(db.String(100))
    name_translations = db.Column(db.String(500))
    cases = Column(db.String(500))


class City(db.Model):
    __tablename__ = 'cities'

    query: sql.Select

    id = db.Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    country_code = db.Column(db.String(10))
    code = db.Column(db.String(10))
    coordinates = db.Column(db.String(200))
    name = db.Column(db.String(100))
    time_zone = db.Column(db.String(100))
    name_translations = db.Column(db.String(100))
    cases = db.Column(db.String(500))


class Preset(db.Model):
    __tablename__ = 'presets'

    query: sql.Select

    id = Column(db.Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(db.String(100))
    raw_query = Column(db.String(1000))
