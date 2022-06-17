from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from src.db.db import engine, meta_data


admins = Table('admins', meta_data,
    Column('id', Integer, primary_key=True),
    Column('name', String(60), nullable=False),
    Column('first_surname', String(60), nullable=False),
    Column('second_surname', String(60), nullable=False),
    Column('telephone', String(15), nullable=False),
    Column('role', String(60), nullable=False),
    Column('registration_tag', String(60), nullable=False),
    Column('email', String(80), nullable=False),
    Column('password',String(300), nullable=False)
)

meta_data.bind = engine
meta_data.create_all()