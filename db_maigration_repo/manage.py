#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(url='mysql://blog:blog@192.168.99.101/blog', debug='False', repository='./db_maigration_repo/')
