from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Date, Time, Boolean
from src.db.db import engine, meta_data


appointments = Table('appointments', meta_data,
    Column('id', Integer, primary_key=True),
    Column('id_user', Integer, foreign_keys=True),
    Column('curp',String(18), nullable=False),
    Column('name',String(60), nullable=False),
    Column('first_surname',String(60), nullable=False),
    Column('second_surname',String(60), nullable=False),
    Column('born_country',String(250), nullable=False),
    Column('born_date',String(250), nullable=False),
    Column('nationality',String(250), nullable=False),
    Column('address',String(250), nullable=False),
    Column('telephone',String(250), nullable=False),
    Column('optional_telephone',String(250), nullable=True),
    
    
    Column('state',String(250), nullable=False),
    Column('office',String(250), nullable=False),
    Column('office_paperwork',String(200), nullable=False),
    Column('identification_document',String(200), nullable=False),
    Column('identification_document_url',String(1000), nullable=False),
    Column('nationality_document',String(200), nullable=False),
    Column('nationality_document_url',String(1000), nullable=False),
    Column('date', Date, nullable=False),
    Column('time', Time, nullable=False),
    Column('status', Boolean, nullable=False),
       
)


meta_data.bind = engine
meta_data.create_all()