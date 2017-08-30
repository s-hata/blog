from sqlalchemy import *
from migrate import *
from migrate.changeset import schema


pre_meta = MetaData()
post_meta = MetaData()

post = Table('post', post_meta,
       Column('id', Integer, primary_key=True, nullable=False),
       Column('body', String(length=140), nullable=False),
       Column('created_at', DateTime, nullable=False),
       Column('created_by', String(length=64), nullable=False),
       Column('updated_at', DateTime, nullable=False),
       Column('updated_by', String(length=64), nullable=False),
       Column('user_id', Integer, ForeignKey("user.id")))

def upgrade(migrate_engine):
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    Table('user', post_meta, autoload=True)
    post_meta.tables[u'post'].create()

def downgrade(migrate_engine):
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables[u'post'].drop()
