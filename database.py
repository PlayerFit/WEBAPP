from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgres://alhqpbkb:WQ-RjLbw5LrkrBMJcFKWWfbaxhsyReTs@babar.elephantsql.com:5432/alhqpbkb')
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

def init_db():
    metadata.create_all(bind=engine)
