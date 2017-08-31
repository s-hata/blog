from sqlalchemy import *
from migrate import *


pre_meta = MetaData()
post_meta = MetaData()

def upgrade(migrate_engine):
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    user = Table('user', post_meta, autoload=True)
    about_me = Column('about_me', String(length=140), nullable=True)
    about_me.create(user)
    last_seen = Column('last_seen', DateTime, nullable=True)
    last_seen.create(user)

def downgrade(migrate_engine):
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    user = Table('user', post_meta, autoload=True)
    user.c.about_me.drop()
    user.c.last_seen.drop()
