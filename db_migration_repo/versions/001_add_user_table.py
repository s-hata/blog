from sqlalchemy import *
from migrate import *
from migrate.changeset import schema


pre_meta = MetaData()
post_meta = MetaData()

user = Table('user', post_meta,
       Column('id', Integer, primary_key=True, nullable=False),
       Column('nickname', String(length=64), nullable=False),
       Column('email', String(length=128), nullable=False),
       Column('created_at', DateTime, nullable=False),
       Column('created_by', String(length=64), nullable=False),
       Column('updated_at', DateTime, nullable=False),
       Column('updated_by', String(length=64), nullable=False))

def upgrade(migrate_engine):
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables[u'user'].create()

def downgrade(migrate_engine):
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables[u'user'].drop()
