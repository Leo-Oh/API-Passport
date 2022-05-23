from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from src.db.db import engine, meta_data


appointments = Table('appointments', meta_data,
    Column('id', Integer, primary_key=True),
    Column('id_user', Integer, foreign_keys=True),
    Column('state',String(250), nullable=False),
    Column('office',String(250), nullable=False),
    Column('curp',String(18), nullable=False),
    Column('office_paperwork',String(200), nullable=False),
    Column('identification_document',String(200), nullable=False),
    Column('identification_document_url',String(1000), nullable=False),
    Column('nationality_document',String(200), nullable=False),
    Column('nationality_document_url',String(1000), nullable=False),
       
)


meta_data.bind = engine
meta_data.create_all()