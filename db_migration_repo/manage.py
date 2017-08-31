#!/usr/bin/env python
import os
import sys

from migrate.versioning.shell import main


path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(path)

from app import app

url = app.config['SQLALCHEMY_DATABASE_URI']
repository = app.config['SQLALCHEMY_MIGRATION_REPO']

if __name__ == '__main__':
    main(url=url, debug='False', repository=repository)
#    main(url='mysql://root@127.0.0.1/circle_test', debug='False', repository='./db_maigration_repo/')
