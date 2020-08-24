from flask_login import UserMixin

from app.db import get_db


class User(UserMixin):
    """
    The User class holds the methods to store and retrieve information from the database 
    about a user, and can be instantiated itself to represent the data of a user. 
    """
    def __init__(self, id_, name, email, profile_pic, calendar_list = []):
        """
        Initalizes the User object with their account information and the calendars
        they possess.
        """
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.calendar_list = calendar_list

    @staticmethod
    def get(user_id):
        """
        Retrieves a user from the database based on the given user_id.
        """
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
        )
        return user

    @staticmethod
    def create(id_, name, email, profile_pic):
        """
        Inserts a user into the database with the given information.
        """
        db = get_db()
        db.execute(
            "INSERT INTO user (id, name, email, profile_pic)"
            " VALUES (?, ?, ?, ?)",
            (id_, name, email, profile_pic),
        )
        db.commit()

    @staticmethod
    def set_calendars(id_, email, calendar_list):
        """
        Inserts all of a user's calendars into the database.
        """
        for calendar_id in calendar_list:
            db.execute(
                "INSERT INTO calendar (id, email, calendar_id)"
                " VALUES (?, ?, ?)",
                (calendar_id, email, id_),
            )
            db.commit()