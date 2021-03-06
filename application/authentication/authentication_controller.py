from flask import request
from flask_restplus import Resource

from application.authentication.authentication_dto import AuthDto
from application.authentication.authentication_service import AuthService

api = AuthDto.api
_user_auth = AuthDto.user_auth


@api.route("/")
class UserSignUp(Resource):
    """
        User Sign Up Resource
    """
    @api.doc("User singing up")
    @api.expect(_user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return AuthService.sign_up_user(data=post_data)
