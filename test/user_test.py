import datetime
import unittest

from app import app, db
from app.models import User, followers

class UserTestCase(unittest.TestCase):

    def setUp(self):
        self.session = db.session

    def tearDown(self):
        self.session.rollback()

    def test_create(self):
        user = User(nickname='nick1',
                    email='nick1@test.com',
                    about_me='about nick1',
                    last_seen=datetime.datetime.utcnow())
        db.session.add(user)
        result = User.query.filter_by(nickname='nick1').first()
        self.assertEqual(result.nickname, 'nick1')

    def test_follow(self):
        followed_user = User(nickname='nick1',
                    email='nick1@test.com',
                    about_me='about nick1',
                    last_seen=datetime.datetime.utcnow())
        follower_user = User(nickname='nick2',
                    email='nick2@test.com',
                    about_me='about nick2',
                    last_seen=datetime.datetime.utcnow())
        self.session.add(follower_user)
        self.session.add(followed_user)
        follower_user.follow(followed_user)
        self.session.add(follower_user)
        #self.assertEqual(followed_user.followed.filter(followers.c.followed_id == followed_user.id).count, 1)
        self.assertEqual(follower_user.followed.filter(followers.c.followed_id == followed_user.id).count(), 1)
