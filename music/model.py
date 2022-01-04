# -*- coding: utf-8 -*-
"""This module contains the data model of the application."""

import datetime
import pkg_resources
pkg_resources.require("SQLAlchemy>=0.4.3")

from turbogears.database import get_engine, metadata, session, mapper
# import the standard SQLAlchemy mapper

#from sqlalchemy.orm import mapper
from sqlalchemy.orm import relationship
from sqlalchemy.orm import relation

# To use the session-aware mapper use this import instead
# from turbogears.database import session_mapper as mapper
# import some basic SQLAlchemy classes for declaring the data model
# (see http://www.sqlalchemy.org/docs/05/ormtutorial.html)

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import String, Unicode, Integer, DateTime, Date, Text

# import some datatypes for table columns from SQLAlchemy
# (see http://www.sqlalchemy.org/docs/05/reference/sqlalchemy/types.html for more)

# your model classes
# http://www.sqlalchemy.org/docs/05/ormtutorial.html#define-a-python-class-to-be-mapped

# class YourDataClass(object):
#     pass


class Artist(object):
    pass

    def __init__(self, id, name, genre_id, country, descr):
        self.artist_id = id
        self.name = name
	self.genre_id = genre_id
        self.country = country
        self.descr = descr

class Genre(object):
    pass

    def __init__(self, id, name, main):
        self.genre_id = id
        self.name = name
	self.main_genre_id = main


class Album(object):
    pass

    def __init__(self, id, title, artist_id, genre_id, year, have, rating, atype, date):
        self.album_id = id
        self.title = title
        self.artist_id = artist_id
        self.year = year
        self.have = have
        self.rating = rating
        self.genre_id = genre_id
        self.atype = atype
        self.date = date
        self.old_id = ""


# your data tables
# http://www.sqlalchemy.org/docs/05/metadata.html

# your_table = Table('yourtable', metadata,
#     Column('my_id', Integer, primary_key=True)
# )

artists = Table('artists', metadata,
    Column('artist_id', Integer, primary_key=True, nullable=False),
    Column('name', Unicode(255), unique=True, nullable=False),
    Column('country', Unicode(255)),
    Column('description', Text),
    Column('genre_id', Integer, ForeignKey("genres.genre_id"))
)

genres_table = Table('genres', metadata,
    Column('genre_id', Integer, primary_key=True, nullable=False),
    Column('name', Unicode(255), unique=True, nullable=False),
    Column('main_genre_id', Integer)
)

albums_table = Table('albums', metadata,
    Column('album_id', Integer, primary_key=True, nullable=False),
    Column('title', Unicode(255), nullable=False),
    Column('artist_id', Integer, ForeignKey("artists.artist_id")),
    Column('old_id', Unicode(5)),
    Column('year', Integer),
    Column('have', Integer),
    Column('rating', Integer),
    Column('genre_id', Integer, ForeignKey("genres.genre_id")),
    Column('atype', Integer),
    Column('date', Date)
)

# set up mappers between your data tables and classes
# http://www.sqlalchemy.org/docs/05/mappers.html

# mapper(YourDataClass, your_table)

mapper(Artist, artists, properties={
    'genre': relationship(Genre, backref='artist')
})
mapper(Genre, genres_table)
mapper(Album, albums_table, properties={
    'artist': relationship(Artist, backref='album'),
    'genre': relationship(Genre, backref='album')
})

# functions for populating the database

def bootstrap_model(clean=False):
    """Create all database tables and fill them with default data.

    This function is run by the 'bootstrap' function from the command module.
    By default it creates all database tables for your model.

    You can add more functions as you like to add more boostrap data to the
    database or enhance the function below.

    If 'clean' is True, all tables defined by your model will be dropped before
    creating them again.

    """
    create_tables(clean)

def create_tables(drop_all=False):
    """Create all tables defined in the model in the database.

    Optionally drop existing tables before creating them.

    """
    get_engine()
    if drop_all:
        print "Dropping all database tables defined in model."
        metadata.drop_all()
    metadata.create_all()

    print "All database tables defined in model created."

