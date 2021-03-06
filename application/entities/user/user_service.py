import datetime
import uuid

from application import db
from application.entities.user.user_model import User


class UserService:
    def __init__(self):
        self.user = None

    def create_user(self, data):
        if UserService._data_verification(data):
            self._create_model_object(data)
        else:
            response_object = {
                "status": "fail",
                "message": "Please give all needed information"
            }
            return response_object, 400

        self._save_changes()

        response_object = {
            "status": "success",
            "public_id": self.user.public_id,
            "message": "Successfully created"
        }
        return response_object, 201

    def load_user(self, public_id):
        self.user = User.query.filter_by(public_id=public_id).first()

    def is_nan_user(self):
        return self.user is None

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    def get_user_public(self):
        return UserService._make_user_public(self.user)

    def get_user_profile(self):
        user_profile = dict(
            public_id=self.user.public_id,
            first_name=self.user.first_name,
            middle_name=self.user.middle_name,
            last_name=self.user.last_name,
            email=self.user.email,
            registered_on=self.user.registered_on,
            admin=self.user.admin,
        )
        return user_profile

    @staticmethod
    def get_all_users():
        return list(map(UserService._make_user_public, User.query.all()))

    def sign_up(self, data):
        self.user = User.query.filter_by(email=data.get("email")).first()
        print(self.user)
        if self.is_nan_user():
            response_object = {
                "status": "fail",
                "message": "password does not match."
            }
            return response_object, 401
        if self._verify_sign_up(data):
            try:
                self.user.email = data.get("email")
                self.user.password = data.get("password")
                response_object = {
                    "status": "success",
                    "message": "Successfully sign up."
                }
                return response_object, 200
            except Exception as e:
                print(e)
                response_object = {
                    "status": "fail",
                    "message": "Try again"
                }
                return response_object, 500

        else:
            response_object = {
                "status": "fail",
                "message": "email or password does not exist."
            }
            return response_object, 401

    def _verify_sign_up(self, data):
        return "email" in data and "password" in data

    @staticmethod
    def _data_verification(data):
        if "first_name" not in data or "last_name" not in data:
            return False
        return True

    def _create_model_object(self, data):
        user_data = data.copy()
        user_data.update(dict(
            public_id=str(uuid.uuid4()),
            verification_code=str(uuid.uuid4()),
            registered_on=datetime.datetime.utcnow()
        ))
        self.user = User(**user_data)

    def _save_changes(self):
        db.session.add(self.user)
        db.session.commit()

    @staticmethod
    def _make_user_public(user):
        user_public = dict(
            public_id=user.public_id,
            first_name=user.first_name,
            middle_name=user.middle_name,
            last_name=user.last_name,
            email=user.email,
        )
        return user_public