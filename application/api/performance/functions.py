from http import HTTPStatus
from datetime import datetime


from flask import current_app, jsonify

from application import db
from application.helpers import token_required
from application.models import (
    Order,
    OrderMobile,
    SellerProfile,
    Feedback,
    CustomerProfile,
    CustomerDeliveryFeedback,
    CustomerUser,
    SellerDeliveryFeedback,
    DeliveryCustomerFeedback,
    DeliverySellerFeedback
)


def deliver_ticket_create():
    pass


def seller_review_create():
    pass


def customer_review_create():
    pass


@token_required
def get_completed_list():
    try:
        deliverer_id = get_completed_list.user_id
        res = []
        orders = (
            db.session.query(
                Order.id,
                Order.ref_no,
                Order.type,
                Order.seller_prof,
                Order.date,
                Order.net,
                OrderMobile.cus_id,
                OrderMobile.is_deliver,
                SellerProfile.organization,
                SellerProfile.street_address,
            )
            .join(OrderMobile, OrderMobile.order_id == Order.id)
            .join(SellerProfile, SellerProfile.id == Order.seller_prof)
            .filter(
                OrderMobile.deliverer_id == deliverer_id, OrderMobile.is_deliver == True
            )
            .all()
        )

        # print(orders)
        for i in orders:
            # order State
            info = {
                "order_id": i.id,
                "Order_ref_no": i.ref_no,
                "seller_name": i.organization,
                "street_address": i.street_address,
                "Order_date": i.date.strftime("%y-%m-%d"),
                "net": i.net,
                "cus_id": i.cus_id,
            }
            res.append(info)

        res = jsonify(res)
        res.status_code = HTTPStatus.CREATED
    except Exception as e:
        res = jsonify(status="fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    return res


@token_required
def get_failed_list():
    try:
        deliverer_id = get_failed_list.user_id
        res = []
        orders = (
            db.session.query(
                Order.id,
                Order.ref_no,
                Order.seller_prof,
                Order.date,
                Order.net,
                OrderMobile.cus_id,
                OrderMobile.is_deliver,
                SellerProfile.organization,
                SellerProfile.street_address,
            )
            .join(OrderMobile, OrderMobile.order_id == Order.id)
            .join(SellerProfile, SellerProfile.id == Order.seller_prof)
            .filter(
                OrderMobile.deliverer_id == deliverer_id,
                OrderMobile.is_deliver == False,
                OrderMobile.is_pick == True,
            )
            .all()
        )

        # print(orders)
        for i in orders:
            # order State
            info = {
                "order_id": i.id,
                "Order_ref_no": i.ref_no,
                "seller_name": i.organization,
                "street_address": i.street_address,
                "Order_date": i.date.strftime("%y-%m-%d"),
                "net": i.net,
                "cus_id": i.cus_id,
            }
            res.append(info)

        res = jsonify(res)
        res.status_code = HTTPStatus.CREATED
    except Exception as e:
        res = jsonify(status="fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    return res


@token_required
def customer_review_create(data):
    customer_id = data.get("customer_id")
    deliverer_id = customer_review_create.user_id
    rate = data.get("rate")
    review = data.get("review")
    order_id = data.get("order_id")
    if order_id == 0:
        order_id = None

    res = {}

    try:
        new_feedback = Feedback(rate=rate, review=review, order_id=order_id)
        db.session.add(new_feedback)
        db.session.flush()
        feedback_id = new_feedback.id
        new_deliverer_customer = DeliveryCustomerFeedback(
            feedback_id=feedback_id, deliverer_id=deliverer_id, cus_id=customer_id
        )
        db.session.add(new_deliverer_customer)
        db.session.commit()

        res = jsonify(status="success", message="review created")
        res.status_code = HTTPStatus.CREATED
    except Exception as e:
        res = jsonify(status="fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    return res


# Get all customer deliverer reviews
@token_required
def get_customer_review():
    try:
        res = []
        deliverer_id = get_customer_review.user_id
        cus_rev = (
            db.session.query(
                Feedback.id, Feedback.rate, Feedback.review, CustomerProfile.first_name
            )
            .join(
                CustomerDeliveryFeedback,
                CustomerDeliveryFeedback.feedback_id == Feedback.id,
            )
            .join(CustomerUser, CustomerUser.id == CustomerDeliveryFeedback.cus_id)
            .join(CustomerProfile, CustomerProfile.cus_id == CustomerUser.id)
            .filter(CustomerDeliveryFeedback.deliverer_id == deliverer_id)
            .limit(50)
        )
        res = []
        for i in cus_rev:
            info = {"first_name": i.first_name, "rate": i.rate, "review": i.review}
            res.append(info)

    except Exception as e:
        res = jsonify(status="fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    return res


# Get all seller deliverer reviews
@token_required
def get_seller_review():
    try:
        res = []
        deliverer_id = get_seller_review.user_id
        cus_rev = (
            db.session.query(
                Feedback.id, Feedback.rate, Feedback.review, SellerProfile.first_name
            )
            .join(
                SellerDeliveryFeedback,
                SellerDeliveryFeedback.feedback_id == Feedback.id,
            )
            .join(SellerProfile, SellerDeliveryFeedback.seller_prof == SellerProfile.id)
            .filter(SellerDeliveryFeedback.deliverer_id == deliverer_id)
            .limit(50)
        )
        res = []
        for i in cus_rev:
            info = {"first_name": i.first_name, "rate": i.rate, "review": i.review}
            res.append(info)

    except Exception as e:
        res = jsonify(status="fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    return res


@token_required
def seller_review_create(data):
    seller_id = data.get("seller_id")
    deliverer_id = seller_review_create.user_id
    rate = data.get("rate")
    review = data.get("review")
    order_id = data.get("order_id")
    if order_id == 0:
        order_id = None

    res = {}

    try:
        new_feedback = Feedback(rate=rate, review=review, order_id=order_id)
        db.session.add(new_feedback)
        db.session.flush()
        feedback_id = new_feedback.id
        new_deliverer_seller = DeliverySellerFeedback(
            feedback_id=feedback_id, deliverer_id=deliverer_id, seller_prof=seller_id
        )
        db.session.add(new_deliverer_seller)
        db.session.commit()

        res = jsonify(status="success", message="review created")
        res.status_code = HTTPStatus.CREATED
    except Exception as e:
        res = jsonify(status="fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    return res
