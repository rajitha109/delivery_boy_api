from datetime import datetime
from http import HTTPStatus
import ast
from os import stat


from flask import current_app, jsonify
from .utils import gen_ref_key


from application import db
from application.helpers import token_required
from application.models import (
    
    DeliveryBank,
    DeliveryPayment,
    DeliveryPaymentCashInHand,
    DeliveryPaymentDeposit,
    DeliveryPaymentArrears,
    Order,
    DeliveryPaymentWithdrawal,
)


@token_required
def save_bank_details(data):
    try:
        bank_name = data.get("bank_name")
        branch = data.get("branch")
        acc_no = data.get("acc_no")
        acc_holder = data.get("acc_holder")
        deliverer_id = save_bank_details.user_id
        res = {}

        new_bank = DeliveryBank(
            bank_name=bank_name,
            branch=branch,
            acc_no=acc_no,
            acc_holder=acc_holder,
            deliverer_id=deliverer_id,
        )
        print(new_bank)
        db.session.add(new_bank)
        db.session.commit()

        res = jsonify(status="success", message="Save Bank Data")
        print(res)

    except Exception as e:
        res = jsonify(Status="Fail", message="acc_no_exists")
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return res


@token_required
def get_bank_details():
    deliverer_id = get_bank_details.user_id
    new_bank_details = DeliveryBank.query.filter_by(deliverer_id=deliverer_id).first()
    return new_bank_details


@token_required
def update_bank_details(data):
    try:
        bank_name = data.get("bank_name")
        branch = data.get("branch")
        acc_no = data.get("acc_no")
        acc_holder = data.get("acc_holder")
        deliverer_id = update_bank_details.user_id
        res = {}

        update_bank = DeliveryBank.query.filter_by(deliverer_id=deliverer_id).first()
        update_bank.bank_name = bank_name
        update_bank.branch = branch
        update_bank.acc_no = acc_no
        update_bank.acc_holder = acc_holder

        print(update_bank)
        db.session.commit()

        res = jsonify(status="success", message="Update Bank Data")

    except Exception as e:
        res = jsonify(Status="Fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return res


@token_required
def delete_bank_details():
    res = {}
    try:
        deliver_id = delete_bank_details.user_id
        bank = DeliveryBank.query.filter_by(deliverer_id=deliver_id).first()
        db.session.delete(bank)
        db.session.commit()

        res = jsonify(status="success", message="delete Bank Data")

    except Exception as e:
        res = jsonify(Status="Fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    return res


@token_required
def get_cash_in_hand():
    deliver_id = get_cash_in_hand.user_id
    res = []
    cash_in_hand_total = 0

    try:
        info = {}
        delivery_payment = (
            db.session.query(
                DeliveryPayment.cash_in_hand,
                DeliveryPaymentCashInHand.pay_id,
                DeliveryPaymentCashInHand.order_id,
            )
            .join(
                DeliveryPaymentCashInHand,
                DeliveryPaymentCashInHand.pay_id == DeliveryPayment.id,
            )
            .filter(
                DeliveryPayment.deliverer_id == deliver_id,
                DeliveryPaymentCashInHand.is_deposit == False,
            )
            .all()
        )

        for i in delivery_payment:
            order_id = i.order_id
            print(order_id)
            order_data = (
                db.session.query(Order.id, Order.net).filter_by(id=order_id).first()
            )
            print(order_data)

            info = {
                "pay_id": i.pay_id,
                "order_id": i.order_id,
                "amount": order_data.net,
            }
            cash_in_hand_total = cash_in_hand_total + order_data.net

            res.append(info)

        info2 = {"total_cash_in_hand": cash_in_hand_total}
        res.append(info2)
        res = jsonify(res)
        res.status_code = HTTPStatus.OK

    except Exception as e:
        res = jsonify(status="fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return res


@token_required
def deposite_cash_in_hand(data):
    cash_list = data.get("cash_in_hand_list")
    transaction_no = data.get("transaction_no")
    res = {}

    deliverer_id = deposite_cash_in_hand.user_id

    try:

        result = ast.literal_eval(cash_list)
        ref_no = gen_ref_key(DeliveryPaymentDeposit, "DPD")
        date = datetime.now()
        amount = 0
        pay_id = 0
        for id, info in result.items():
            for key in info:
                order_id = key
                pay_id = info[key]

            print(" order_id: " + order_id, "pay_id: " + pay_id)
            order_data = (
                db.session.query(Order.id, Order.net).filter_by(id=order_id).first()
            )
            amount = amount + order_data.net
        print(amount)

        # deposite cash in hand
        new_deposite = DeliveryPaymentDeposit(
            ref_no=ref_no,
            amount=amount,
            date=date,
            transaction_no=transaction_no,
            pay_id=pay_id,
        )
        db.session.add(new_deposite)
        db.session.flush()

        # update cash in hand
        delivery_payment = (
            db.session.query(DeliveryPayment)
            .filter_by(deliverer_id=deliverer_id)
            .first()
        )
        cash = delivery_payment.cash_in_hand
        delivery_payment.cash_in_hand = cash - amount
        print(delivery_payment.cash_in_hand)
        db.session.commit()

        res = jsonify(
            status="success",
            message="deposited",
        )

        res.status_code = HTTPStatus.CREATED

    except Exception as e:
        res = jsonify(status="fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return res


@token_required
def get_deposited_list():
    deliver_id = get_deposited_list.user_id
    res = []

    try:
        info = {}
        deposited_cih = (
            db.session.query(
                DeliveryPaymentDeposit.id,
                DeliveryPaymentDeposit.ref_no,
                DeliveryPaymentDeposit.amount,
                DeliveryPaymentDeposit.date,
                DeliveryPaymentDeposit.transaction_no,
            )
            .join(DeliveryPayment, DeliveryPayment.id == DeliveryPaymentDeposit.pay_id)
            .filter(DeliveryPayment.deliverer_id == deliver_id)
            .all()
        )
        for i in deposited_cih:

            info = {
                "ref_no": i.ref_no,
                "deposited_amount": i.amount,
                "date": i.date.strftime("%y-%m-%d"),
                "transaction_no": i.transaction_no,
            }

            res.append(info)

        res = jsonify(res)
        res.status_code = HTTPStatus.OK

    except Exception as e:
        res = jsonify(status="fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return res


@token_required
def create_withdrawal_request(data):
    withdraw_list = data.get("withdraw_list")
    note=data.get("note")
    deliver_id = create_withdrawal_request.user_id
    res = {}
    message = ""
    total_amount = 0
    arrears = 0
    result = ast.literal_eval(withdraw_list)
    ref_no = gen_ref_key(DeliveryPaymentWithdrawal, "DPW")
    date = datetime.now()

    p_id = 0

    try:
        #get current arrears
        arrears_q = (
            db.session.query(
                DeliveryPaymentArrears.id,
                DeliveryPaymentArrears.amount,
                DeliveryPaymentArrears.order_id,
                DeliveryPaymentArrears.pay_id,
                DeliveryPaymentArrears.withdrawl_id,
                DeliveryPayment.arrears,
                DeliveryPayment.id,
            )
            .join(DeliveryPayment, DeliveryPayment.id == DeliveryPaymentArrears.pay_id)
            .filter(
                DeliveryPayment.deliverer_id == deliver_id,
                DeliveryPaymentArrears.is_receive == False,
                DeliveryPaymentArrears.is_deduct == False,
                DeliveryPaymentArrears.withdrawl_id == None,
            )
            .all()
        )

        for i in arrears_q:
            arrears = i.arrears            
            p_id=i.pay_id       
        
        #check whether arrears is greater than MIN_WITHDRAWAL_AMOUNT
        if arrears >= current_app.config.get("MIN_WITHDRAWAL_AMOUNT"):
            #create new DeliveryPaymentWithdrawal
            new_withdraw=DeliveryPaymentWithdrawal(ref_no=ref_no,amount=0,date=date,note=note,pay_id=p_id)
            db.session.add(new_withdraw)            
            db.session.flush()
            

            # update arrears in DeliveryPayment
            delivery_payment = (
                db.session.query(DeliveryPayment)
                .filter_by(deliverer_id=deliver_id)
                .first()
            )
                      

            #update deliverypaymentarrears
            for id, info in result.items():
                for key in info:
                    ord_id = key
                    pay_id = info[key]

                delivery_payment_arrears=db.session.query(DeliveryPaymentArrears).filter_by(order_id=ord_id).first()
                total_amount=total_amount+delivery_payment_arrears.amount                
                delivery_payment_arrears.withdrawl_id=new_withdraw.id
                db.session.flush()
                

                status='success'
                message="send_request"
            
            #update withdraw amount
            new_withdraw.amount=total_amount
            delivery_payment.arrears = arrears - total_amount
            db.session.commit()

        else:
            status='fail'
            message="insufficient"

                

        res = jsonify(status=status, message=message)
        res.status_code = HTTPStatus.OK

    except Exception as e:
        
        res = jsonify(status="fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return res


@token_required
def get_arrears_list():
    deliver_id = get_arrears_list.user_id
    res = []
    total_amount = 0
    arrears = 0

    try:
        info = {}
        withdraw_q = (
            db.session.query(
                DeliveryPaymentArrears.id,
                DeliveryPaymentArrears.amount,
                DeliveryPaymentArrears.is_receive,
                DeliveryPaymentArrears.is_deduct,
                DeliveryPaymentArrears.order_id,
                DeliveryPaymentArrears.pay_id,
                DeliveryPaymentArrears.withdrawl_id,
                DeliveryPayment.arrears,
                DeliveryPayment.id,
            )
            .join(DeliveryPayment, DeliveryPayment.id == DeliveryPaymentArrears.pay_id)
            .filter(
                DeliveryPayment.deliverer_id == deliver_id,
                DeliveryPaymentArrears.is_receive == False,
                DeliveryPaymentArrears.is_deduct == False,
                DeliveryPaymentArrears.withdrawl_id == None,
            )
            .all()
        )

        for i in withdraw_q:
            print(i.arrears)
            arrears = i.arrears
            total_amount = total_amount + i.amount

            info = {"amount": i.amount, "order_id": i.order_id, "pay_id": i.pay_id}

            res.append(info)
        info2 = {"total_amnount": arrears}
        res.append(info2)
        res = jsonify(res)
        res.status_code = HTTPStatus.OK

    except Exception as e:
        res = jsonify(status="fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return res



@token_required
def get_withdrawal_list():
    deliver_id = get_withdrawal_list.user_id
    res = [] 
    state='pending'   

    try:
        info = {}
        withdrawal_list_q = (
            db.session.query(
                DeliveryPaymentWithdrawal.id,
                DeliveryPaymentWithdrawal.ref_no,
                DeliveryPaymentWithdrawal.amount,
                DeliveryPaymentWithdrawal.date,
                DeliveryPaymentWithdrawal.is_complete,
                DeliveryPaymentWithdrawal.is_cancel,
                DeliveryPayment.id,
            )
            .join(DeliveryPayment, DeliveryPayment.id == DeliveryPaymentWithdrawal.pay_id)
            .filter(
                DeliveryPayment.deliverer_id == deliver_id
            )
            .all()
        )

        for i in withdrawal_list_q:
            if i.is_complete==True:
                state='complete'
            elif i.is_cancel==True:
                state='cancel'
            else:
                state='pending'

            info = {"ref_no":i.ref_no,"amount": i.amount, "date": i.date.strftime("%y-%m-%d"), "state": state}

            res.append(info)        
       
        res = jsonify(res)
        res.status_code = HTTPStatus.OK

    except Exception as e:
        res = jsonify(status="fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return res

#withdraw receive action
@token_required
def create_withdrawal_receive():
    try:
        pass
        print("withdraw")

        res = jsonify(status="success")
        print(res)

    except Exception as e:
        res = jsonify(Status="Fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return res
