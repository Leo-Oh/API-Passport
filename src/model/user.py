from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from src.db.db import engine, meta_data


users = Table('users', meta_data,
    Column('id', Integer, primary_key=True),
    Column('curp', String(18), nullable=False),
    Column('email', String(60), nullable=False),
    Column('password',String(250), nullable=False)
)


meta_data.bind = engine
meta_data.create_all()