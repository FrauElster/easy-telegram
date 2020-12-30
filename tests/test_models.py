from easy_telegram.models.Permission import Permission
from easy_telegram.models.User import User
from easy_telegram.util.SessionHandler import SessionHandler
from tests.Mock import FACTORY


class TestModels:
    def test_user_exists(self):
        username = FACTORY.get_user_user_name()

        session = SessionHandler().session
        session.add(User(name=username, permissions=[], whitelisted=True))
        session.commit()

        assert User.exists(name=username)

    def test_user_get_or_create(self):
        username = FACTORY.get_user_user_name()
        User.get_or_create(name=username)
        session = SessionHandler().session
        user_count = len(session.query(User).all())

        User.get_or_create(name=username)
        assert user_count == len(session.query(User).all())

        new_username = FACTORY.get_user_user_name()
        User.get_or_create(name=new_username)
        assert user_count + 1 == len(session.query(User).all())

    def test_is_admin(self):
        session = SessionHandler().session
        admin_perm = Permission.get_or_create(session, name="admin")
        admin_user = User(name="admin_user", permissions=[admin_perm], whitelisted=True)
        session.commit()  # pylint: disable=E1101

        assert admin_user.is_admin
