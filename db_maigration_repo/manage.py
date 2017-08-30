#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(url='mysql://root@127.0.0.1/circle_test', debug='False', repository='./db_maigration_repo/')
