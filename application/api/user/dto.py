
from flask_restx import Model
from flask_restx.inputs import email
from flask_restx.fields import String, Boolean, Integer, Float
from flask_restx.reqparse import RequestParser
from werkzeug.datastructures import FileStorage

# 
# ---------------------------------------------Models-----------------------------------------------------------------------------
# 

user_model = Model(
    'DeliveryUser',
    {
        'contact_no': String,
        "public_id": String,
        "is_confirm": Boolean,
        "is_logged_in": Boolean,
        "is_inactive": Boolean,
        "token_expires_in": String,
    }
)

prof_model = Model(
    'DeliveryProfile',
    {
        'id':Integer,
        'nic':String,
        'first_name':String,
        'last_name':String,
        'email': String,
        'street_address':String,
        'city_address':String,
        'postcode':String,     


    }
)

vehicle_model= Model(
    'DeliveryVehicle',
    {
        'id':Integer,
        'type':String,
        'reg_no':String,
        'note':String
    }
)

#
# ---------------------------------------Request parsers--------------------------------------------------------------------------
# 

# Use on register
reg_parser = RequestParser(bundle_errors=True)
reg_parser.add_argument('contact_no', type=str, location="json", required=True, nullable=False, help="Contact No in international format.")
reg_parser.add_argument('player_id', type=str, location="json", required=True, nullable=False, help="One signal player id")

# Use on login
# Will inherit contract no from reg_parser
login_parser = reg_parser.copy()
login_parser.add_argument('conf_code', type=str, location="json", required=True, nullable=False, help="4 digit confimation code")
login_parser.add_argument('counter', type=str, location="json", required=True, nullable=False, help="Hashed code")
login_parser.remove_argument('player_id')


# User on profile
prof_parser = RequestParser(bundle_errors=True)
prof_parser.add_argument('first_name', type=str, location="json", required=True, nullable=False, help="First name, min=3, max=50")
prof_parser.add_argument('last_name', type=str, location="json", required=True, nullable=False, help="Last name, min=3, max=50")
prof_parser.add_argument('email', type=email(), location="json", required=True, nullable=False, help="max=120")
prof_parser.add_argument('nic', type=str, location="json", required=True, nullable=False, help="nic")
prof_parser.add_argument('street_address', type=str, location="json", required=True, nullable=False, help="street_address")
prof_parser.add_argument('city_address', type=str, location="json", required=True, nullable=False, help="city_address")
prof_parser.add_argument('postcode', type=str, location="json", required=True, nullable=False, help="postcode")

#prof_parser.add_argument('image', type=FileStorage, location='files', help="File allowed PNG, JPG, JPEG")


#Deliverer Vehicle
vehicle_parser = RequestParser(bundle_errors=True)
vehicle_parser.add_argument('type', type=str, location="json", required=True, nullable=False, help="type,max=8")
vehicle_parser.add_argument('reg_no', type=str, location="json", required=True, nullable=False, help="reg no, max=10")
vehicle_parser.add_argument('note', type=str, location="json", required=False, nullable=True, help="note, max=100")
