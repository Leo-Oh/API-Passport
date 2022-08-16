from sqlalchemy import create_engine, MetaData


#engine = create_engine('mysql+pymysql://root:password@127.0.0.1:3306/passport')

conn = engine.connect()
meta_data = MetaData()
