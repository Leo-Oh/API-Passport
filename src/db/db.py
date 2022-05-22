from sqlalchemy import create_engine, MetaData



engine = create_engine('mysql+pymysql://root:password@34.94.79.113:3306/passport')

conn = engine.connect()

meta_data = MetaData()
