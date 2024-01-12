from unittest import TestCase

from app import app
from models import db, Users

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UsersViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add 2 sample users."""

        Users.query.delete()

        user1 = Users(first_name="Test", last_name="userone")
        user2 = Users(first_name="Example", last_name="usertwo")

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        self.user1_id = user1.id
        self.user2_id = user2.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test', html)
            self.assertIn('Example', html)

    def test_show_user_details(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user1_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test userone</h1>', html)
            self.assertIn('<img src="https://i.stack.imgur.com/34AD2.jpg" alt="User Profile Image" />', html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "Testy", "last_name": "McTestface", "img_url": ''}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Testy McTestface", html)

    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first_name": "Edity", "last_name": "McEditface", "img_url": 'https://nick-intl.mtvnimages.com/uri/mgid:file:gsp:kids-assets:/nick/properties/spongebob-squarepants/characters/plankton-character-web-desktop.png'}
            resp = client.post(f'/users/{self.user2_id}/edit', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Edity McEditface', html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f'/users/{self.user1_id}/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Test userone', html)

