from email import message
from os import stat
import re
from random import randint
from datetime import datetime
from http import HTTPStatus
from flask import current_app, jsonify

from application import db
from application.models import DeliveryUser, DeliveryProfile, DeliveryVehicle,DeliveryBlacklistToken
from application.helpers import token_required
from application.util.datetime_util import remaining_fromtimestamp, format_timespan_digits
from application.util.otp import Hotp
from .utils import gen_ref_key, save_image, delete_image, parse_push_notification


# Create new user
# Check if user is alredy registered
# If no crete user with mobile number 
def register(data):

    contact_no = re.sub("[^0-9]", "", data.get("contact_no")) # Format contact number in to vaild form "94xxxxxxx"
    user = DeliveryUser.query.filter_by(contact_no = contact_no).first()
    player_id = [data.get("player_id")]

    res = {}

    try:
        
        # Gererate random interger and encrypt
        counter = randint(10000, 99999)
        conf_code = Hotp.otp_gen(counter)
        message = ''

        if user:
            message="existing_user"
           
        else:
            # Create user
            new_user = DeliveryUser(
                contact_no = contact_no
            )
            db.session.add(new_user)
            db.session.commit()

            message="new_user"

        res = jsonify(
            status="success",
            message=message,
            conf_code=conf_code, # Remove on production
            counter = counter
        )
        # Send push notification
        payload = {
            "app_id":current_app.config.get('ONESIGNAL_APP_ID'),
            "contact_no":contact_no,
            "include_player_ids": player_id,
            "contents": {
                "en": conf_code+" is your gogett verification code",
            },
            "name": "gogett User Verification",
            "filters": [
                {"field": "tag", "key": "level", "relation": "=", "value": "10"},
                {"field": "amount_spent", "relation": ">","value": "0"}
            ]
        }
        parse_push_notification.apply_async(args=[payload])
        
        res.status_code = HTTPStatus.CREATED
    except Exception as e: 
        print(e)
        res = jsonify(
            status="fail",
            message=str(e)
        )
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    
    res.headers["Cache-Control"] = "no-store"
    res.headers["Pragma"] = "no-cache"

    return res


# Login user
# If user is not mobile no is not confirmed, confirm and login 
def login(data):
    
    contact_no = re.sub("[^0-9]", "", data.get("contact_no")) # Format contact number in to vaild form "94xxxxxxx"
    counter = int(data.get('counter'))

    user = DeliveryUser.query.filter_by(contact_no = contact_no).first()

    res = {}
    try:
        if user and Hotp.otp_verify(data.get('conf_code'), counter):
            #  Set login true on login manage
            if user.is_confirm == False:
                user.is_confirm = True
                user.confirm_date = datetime.today()
            # Set user to ;pgged in
            user.is_logged_in = True
            db.session.commit()

            print("hello")
            
            access_token = user.encode_access_token()
            print(access_token)

            res = jsonify(
                status="success",
                message="successfully_logged_in",
                access_token=access_token,
                token_type="bearer",
                expires_in=_get_token_expire_time(),
            )
            res.status_code = HTTPStatus.OK
        else:
            res = {
                'status':"fail",
                'message':'erro in login',
            }
            res.status_code = HTTPStatus.FORBIDDEN
    except Exception as e: 
        res = jsonify(
            status="fail",
            message=str(e)
        )
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    res.headers["Cache-Control"] = "no-store"
    res.headers["Pragma"] = "no-cache"

    return res


# Calulate and token expier time
def _get_token_expire_time():
    token_age_h = current_app.config.get("TOKEN_EXPIRE_HOURS")
    token_age_m = current_app.config.get("TOKEN_EXPIRE_MINUTES")
    expires_in_seconds = token_age_h * 3600 + token_age_m * 60
    return expires_in_seconds


# Get logged in user details
@token_required
def get_logged_in_user():
    public_id = get_logged_in_user.public_id
    user = DeliveryUser.query.filter_by(public_id = public_id).first()
    expires_at = get_logged_in_user.expires_at
    user.token_expires_in = format_timespan_digits(remaining_fromtimestamp(expires_at))
    return user


# Logout user
@token_required
def logout():
    access_token = logout.token
    expires_at = logout.expires_at
    # Blacklist tocken
    blacklisted_token = DeliveryBlacklistToken(access_token, expires_at)
    db.session.add(blacklisted_token)
    # Update user login state
    public_id = logout.public_id
    user = DeliveryUser.query.filter_by(public_id = public_id).first()
    user.is_logged_in = False
    db.session.commit()
    response_dict = dict(status="success", message="successfully logged out")
    return response_dict, HTTPStatus.OK


# Create or update profile
@token_required
def profile_save(data):
    user_id = profile_save.user_id
    f_name = data.get('first_name')
    l_name = data.get('last_name')
    email = data.get('email')
    image = data.get('image')

    prof = DeliveryProfile.query.filter_by(deliverer_id = user_id).first()
    new_email = True
    res = {}

    try:
        prof_image = None
        if prof:
            if prof.email == email:
                new_email = False
            if image:
                
                # Delete existion image from file if image is not default avatar
                if prof.image != "default_avatar.png":                    
                    delete_image(prof.image)
                # Save image
                print(prof.image)
                prof_image = save_image(image)
                prof.image = prof_image
            prof.email = email
            prof.first_name = f_name
            prof.last_name = l_name
            db.session.commit()
        else:
            ref_no = gen_ref_key(DeliveryProfile, 'DP')
            if image:
                prof_image = save_image(image)
            new_profile = DeliveryProfile(
                ref_no = ref_no,
                email = email,
                first_name = f_name,
                last_name = l_name,
                image = prof_image,
                cus_id = user_id
            )
            db.session.add(new_profile)
            db.session.commit()
        res = jsonify(
            status_code = HTTPStatus.OK,
            status = "success",
            message = 'Profile_save',
            new_email = new_email
        )
    except Exception as e: 
        res = jsonify(
            status="fail",
            message=str(e)
        )
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return res


# Get profile of customer
@token_required
def get_profile():
    user_id = get_profile.user_id
    prof = DeliveryProfile.query.filter_by(deliverer_id=user_id).first()
    return prof

####### Vehicle#####

# Create  or update vehicle profile
@token_required
def vehicle_profile_save(data):
    user_id = vehicle_profile_save.user_id
    type = data.get('type')
    reg_no = data.get('reg_no')
    note = data.get('note')  

    res = {}
    message=''
    status=''

    try:
        vehicle=DeliveryVehicle.query.filter_by(reg_no=reg_no).first()   
        print(vehicle)    
        if vehicle:
            vehicle.note=note            
            print(vehicle.note)
            vehicle.type=type
            status = "updated",
            message="existing_vehicle"
            db.session.commit() 

        else:
            new_vehicle_profile=DeliveryVehicle(type=type,reg_no=reg_no,note=note,deliverer_id=user_id)
            db.session.add(new_vehicle_profile)
            db.session.commit()            
            message="new_vehicle"
            status = "success"
        
        
           
        res = jsonify(
            status_code = HTTPStatus.OK,
            status = status,
            message = message,
            type = type,
            reg_no=reg_no,
            note=note
        )
    except Exception as e: 
        res = jsonify(
            status="fail",
            message=str(e)
        )
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return res


# Get profile of customer
@token_required
def get_vehicle_profile():
    user_id = get_vehicle_profile.user_id
    prof = DeliveryVehicle.query.filter_by(deliverer_id=user_id).all()
    return prof


