from sqlalchemy import create_engine,MetaData

engine = create_engine("sqlite:///test.db")
meta = MetaData()
conn = engine.connect()