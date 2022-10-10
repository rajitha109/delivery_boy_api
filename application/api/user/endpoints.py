from http import HTTPStatus

from flask_restx import Namespace, Resource

from .dto import (login_parser, prof_model, prof_parser, reg_parser,
                  user_model, vehicle_model, vehicle_parser)
from .functions import (get_logged_in_user, get_profile, login,  # get_location
                        logout, profile_save, register,vehicle_profile_save,get_vehicle_profile)

user_ns = Namespace(name="user", validate=True)

user_ns.models[user_model.name] = user_model
user_ns.models[vehicle_model.name] = vehicle_model
user_ns.models[prof_model.name] = prof_model


# Register user
# Trigger on new user access or login user
@user_ns.route("/register", endpoint="user_register")
class RegisterUser(Resource):
    """Handles HTTP requests to URL: /api/v1/user/register"""
    # Create user
    @user_ns.expect(reg_parser)
    @user_ns.response(int(HTTPStatus.CREATED), "New user was successfully created.")
    @user_ns.response(int(HTTPStatus.CONFLICT), "Email address is already registered.")
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @user_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Register user"""
        data = reg_parser.parse_args()
        res = register(data)
        return res


# Login user
# Trigger after conf code sent to mobile number
@user_ns.route("/login", endpoint="user_login")
class LoginUser(Resource):
    """Handles HTTP requests to URL: /api/v1/user/login"""
    # Create user
    @user_ns.expect(login_parser)
    @user_ns.response(int(HTTPStatus.OK), "Login succeeded.")
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), "email or password does not match")
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @user_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """login user"""
        data = login_parser.parse_args()
        res = login(data)
        return res


# Get user by public id
@user_ns.route("/get", endpoint="user_get")
class GetUser(Resource):
    """Handles HTTP requests to URL: /api/v1/user/get."""

    @user_ns.doc(security="Bearer")
    @user_ns.response(int(HTTPStatus.OK), "Token is currently valid.", user_model)
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @user_ns.marshal_with(user_model)
    def get(self):
        """Validate access token and return user info."""
        return get_logged_in_user()


#  Logout user
@user_ns.route("/logout", endpoint="user_logout")
class LogoutUser(Resource):
    """Handles HTTP requests to URL: /api/v1/user/logout."""

    @user_ns.doc(security="Bearer")
    @user_ns.response(int(HTTPStatus.OK), "Token is currently valid.", user_model)
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @user_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Add token to blacklist, deauthenticating the current user."""
        return logout()


# User profile manage
@user_ns.route("/profile", endpoint="user_profile")
class Profile(Resource):
    """Handles HTTP requests to URL: /api/v1/user/profile"""

    # Get profile of saved by user
    @user_ns.doc(security="Bearer")
    @user_ns.response(int(HTTPStatus.OK), "Token is currently valid.", prof_model)
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @user_ns.marshal_with(prof_model)
    def get(self):
        """Profile saved by user"""
        return get_profile()
        


    @user_ns.doc(security="Bearer")
    @user_ns.expect(prof_parser)
    @user_ns.doc(
        params={
            "first_name": "First name, String, min=3, max=50",
            "last_name": "Last name, String, min=3, max=5",
            "email": "Email, String, max=120, Save in Firebase",
            "image":"File allowed PNG, JPG, JPEG"
        }
    )
    @user_ns.response(int(HTTPStatus.OK), "Profile saved.")
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @user_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        "Create or Update user profile"
        data = prof_parser.parse_args()
        res = profile_save(data)
        return res


# Vehicle Profile manage
@user_ns.route("/vehicle",endpoint="vehicle_profile")
class Vehicle(Resource):
    """Handles HTTP request to URL: /api/v1/user/vehicle """

    #Save vehicle
    @user_ns.doc(security="Bearer")
    @user_ns.response(int(HTTPStatus.OK),"Token is currently valid",vehicle_model)
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @user_ns.response(int(HTTPStatus.UNAUTHORIZED),"Token is invalid or expired.")
    @user_ns.marshal_with(vehicle_model)
    def get(self):
        """Vehicle Profile saved by user"""
        return get_vehicle_profile()

    @user_ns.doc(security="Bearer")
    @user_ns.expect(vehicle_parser)
    @user_ns.doc(
        params={
        "type":"String",
        "reg_no":"String",
        }
    )
    @user_ns.response(int(HTTPStatus.OK), "Profile saved.")
    @user_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @user_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        "Register or Update  Vehicle"
        data = vehicle_parser.parse_args()
        return vehicle_profile_save(data)






    

