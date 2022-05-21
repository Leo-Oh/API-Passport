import string
from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from db.db import engine, meta_data


users = Table('users', meta_data,
    Column('id', Integer, primary_key=True),
    Column('country',String(200), nullable=False),
    Column('state',String(250), nullable=False),
    Column('default_office',String(200), nullable=False),
    Column('born_country', String(200),nullable=False),
    Column('nationality',String(200), nullable=False),
    Column('name', String(60), nullable=False),
    Column('first_surname', String(30), nullable=False),
    Column('second_surname', String(30), nullable=False),
    Column('telephone', String(15), nullable=False),
    Column('optional_telephone', String(15), nullable=True),
    Column('email', String(60), nullable=False),
    Column('password',String(250), nullable=False)
)


meta_data.bind = engine
meta_data.create_all()