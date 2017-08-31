from sqlalchemy import *
from migrate import *
from migrate.changeset import schema


meta = MetaData()

followers = Table('followers', meta,
        Column('follower_id', Integer, ForeignKey('user.id')),
        Column('followed_id', Integer, ForeignKey('user.id')))

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    Table('user', meta, autoload=True)
    meta.tables[u'followers'].create()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    meta.tables[u'followers'].drop()
