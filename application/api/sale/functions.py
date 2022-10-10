from http import HTTPStatus
from datetime import datetime



from flask import current_app, jsonify
from application import db

from .utils import gen_ref_key
from application.models import (
    OrderMobile,
    Order,
    SellerProfile,
    CustomerUser,
    CustomerProfile,
    SellerUser,
    OrderGrocery,
    GroceryProduct,
    OrderFood,
    OrderFoodTaxonomy,
    FoodTaxonomy,
    Food,
    OrderReturn,
    OrderReturnGrocery,
    OrderPaymentDetails,
    OrderPayment,
    DeliveryPayment,
    DeliveryPaymentCashInHand,
    


)


from application.helpers import token_required


@token_required
def create_accept_order(data):
    try:
        res={}
        ord_id=data.get("order_id")
        order_m=db.session.query(OrderMobile).filter_by(order_id=ord_id).first()
        print(order_m)
        deliverer_id=create_accept_order.user_id
        order_m.deliverer_id=deliverer_id
        db.session.commit()


        res = jsonify(
            status="success",
            message="accept",
        )
    except Exception as e:
        res = jsonify(status="fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return res



@token_required
def create_pickup_order(data):
    try:
        ord_id=data.get("order_id")
        res = {}
        order_m = db.session.query(OrderMobile).filter_by(order_id=ord_id).first()
        print(order_m)
        order_m.is_pick = True
        db.session.commit()
        

        res = jsonify(
            status="success",
            message="picked",
        )

    except Exception as e:
        res = jsonify(status="fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return res




@token_required
def get_order_details(order_id):
    try:
        res = []
        res2 = {}
        deliver_id = get_order_details.user_id
        #print(deliver_id)

        # order details
        order_q = (
            db.session.query(
                Order.id.label("order_id"),
                Order.ref_no,
                Order.seller_prof,
                Order.type,
                Order.date,
                Order.net,
                OrderMobile.is_pick,
                OrderMobile.is_deliver,
                OrderMobile.latitude,
                OrderMobile.longitude,
                OrderMobile.cus_id,
            )
            .join(OrderMobile, OrderMobile.order_id == Order.id)
            .filter(Order.id == order_id, OrderMobile.deliverer_id == deliver_id)
            .first()
        )
        print(order_q.is_pick)

       
    
        # order State
        is_pick= order_q.is_pick           
        is_deliver = order_q.is_deliver
        
        
        
        if is_pick == True and is_deliver==False:
            state = "picked"
        elif is_pick == True and is_deliver == True:
            state = "delivered"
        else:
            state = "pending"
        


        # get customer details
        cus_q = (
            db.session.query(
                CustomerUser.id.label("cus_id"),
                CustomerUser.contact_no,
                CustomerProfile.ref_no,
                OrderMobile.order_id,
            )
            .join(OrderMobile, OrderMobile.cus_id == CustomerUser.id)
            .join(CustomerProfile, CustomerProfile.cus_id == CustomerUser.id)
            .filter(CustomerUser.id == order_q.cus_id)
            .first()
        )

        #print(cus_q)

        # seller details
        seller_q = (
            db.session.query(
                SellerUser.id.label("seller_id"),
                SellerProfile.first_name,
                SellerProfile.contact_no,
                SellerProfile.organization,
                SellerProfile.ref_no,
                Order.id,
            )
            .join(SellerProfile, SellerProfile.seller_id == SellerUser.id)
            .join(Order,Order.seller_prof==SellerProfile.seller_id)
            .filter(SellerProfile.id == order_q.seller_prof)
            .first()
        )
        #print(seller_q)

        if order_q.type == "g":
            # get order_grocery details
            order_grocery = (
                db.session.query(
                    OrderGrocery.qty,
                    OrderGrocery.total,
                    OrderGrocery.product_id,
                    GroceryProduct.name,
                )
                .join(GroceryProduct, GroceryProduct.id == OrderGrocery.product_id)
                .filter(OrderGrocery.order_id == order_id)
                .all()
            )

            for i in order_grocery:

                info = {"product_name": i.name, "qty": i.qty, "Total": i.total}
                res.append(info)

        elif order_q.type == "f":
            # get order_food details
            order_Food = (
                db.session.query(
                    OrderFood.id,
                    OrderFood.qty,
                    OrderFood.total,
                    OrderFood.food_id,
                    Food.name,
                )
                .join(Food, Food.id == OrderFood.food_id)
                .filter(OrderFood.order_id == order_id)
                .all()
            )

            for i in order_Food:
                info = {"food_name": i.name, "qty": i.qty, "Total": i.total}
                res.append(info)      
                print(i.id)


                order_Food_tax = (
                    db.session.query(
                        OrderFoodTaxonomy.taxonomy,
                        OrderFoodTaxonomy.content,
                        FoodTaxonomy.description,
                        OrderFoodTaxonomy.food_order_id
                    )
                    .join(FoodTaxonomy, FoodTaxonomy.term_id == OrderFoodTaxonomy.term_id)
                    .filter(
                        OrderFoodTaxonomy.food_order_id == i.id,
                        OrderFoodTaxonomy.taxonomy == "addon",
                    )
                    .all()
                )

            for i in order_Food_tax:
                    info2 = {"addon_price": i.content["price"], "addon_qty": i.content["qty"]}
                    res.append(info2)

           

        res2 = {
            "net_price": order_q.net,
            "state": state,
            "order_id":order_q.order_id,
            "Order_ref_no":order_q.ref_no,
            "order_date": order_q.date.strftime("%y-%m-%d"),
            "order_longitude": order_q.longitude,
            "order_latitude": order_q.latitude,
            "Customer_ref_no": cus_q.ref_no,
            "Customer_contact_no": cus_q.contact_no,
            "Sellet_contact_no": seller_q.contact_no,
            "seller_ref": seller_q.ref_no,
        }

        res.append(res2)
        res = jsonify(res)
        res.status_code = HTTPStatus.CREATED
    except Exception as e:
        res = jsonify(status="fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    return res


@token_required
def create_order_deliver(data):
    try:
        deliver_id=create_order_deliver.user_id
        ord_id = data.get("order_id")
        res = {}
        order_m = db.session.query(OrderMobile).filter_by(order_id=ord_id).first()
        order_m.is_deliver = True

        order_payment_q=(
            db.session.query(
                OrderPayment.id.label('pay_id'),Order.id.label('order_id'),Order.net)
                .join(OrderPayment,OrderPayment.order_id==Order.id)
                .filter(Order.id==ord_id).subquery()
        )
        
        order_pay_details_q=(
            db.session.query(
                OrderPaymentDetails.method,order_payment_q.c.pay_id,order_payment_q.c.order_id,order_payment_q.c.net)
                .join(order_payment_q,order_payment_q.c.pay_id == OrderPaymentDetails.pay_id)
                .first()
        )

        if order_pay_details_q.method == current_app.config.get("PAYMENT_METHODS")["COD"]:
            
            #Cash in hand
            delivery_pay=db.session.query(DeliveryPayment).filter_by(deliverer_id=deliver_id).first()
            delivery_pay_id=0

            if delivery_pay:
                delivery_pay_id=delivery_pay.id
                cash=delivery_pay.cash_in_hand
                delivery_pay.cash_in_hand = cash + order_pay_details_q.net
                db.session.flush()
                

            else:
                cash=float(order_pay_details_q.net)
                delivery_payment=DeliveryPayment(cash_in_hand=cash,deliverer_id=deliver_id)
                db.session.add(delivery_payment)
                db.session.flush()
                delivery_pay_id=delivery_payment.id
                               

            #add to DeliveryPaymentCashInHand
            new_deliver_payment_cih=DeliveryPaymentCashInHand(pay_id=delivery_pay_id,order_id=ord_id)
            db.session.add(new_deliver_payment_cih)
                
            print(new_deliver_payment_cih.id)            
            db.session.commit()

        

        res = jsonify(
            status="success",
            message="delivered",
        )

    except Exception as e:
        res = jsonify(status="fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return res

@token_required
def get_order_list():
    try:
        deliverer_id = get_order_list.user_id
        res = []
        state=''
        orders = (
            db.session.query(
                Order.id,
                Order.type,
                Order.is_complete,
                Order.is_cancel,
                Order.seller_prof,
                Order.date,
                Order.net,
                OrderMobile.is_accept,
                OrderMobile.cus_id,
                OrderMobile.is_pick,
                OrderMobile.is_recive,
                OrderMobile.is_ready,
                OrderMobile.is_deliver,
                SellerProfile.organization,
                SellerProfile.street_address,
            )
            .join(SellerProfile, SellerProfile.id == Order.seller_prof)
            .join(OrderMobile, OrderMobile.order_id == Order.id)
            .filter(OrderMobile.deliverer_id == deliverer_id)
            .all()
        )

        # print(orders)
        for i in orders:

            # order State
          
            is_deliver = i.is_deliver
            is_pick = i.is_pick         
            
           
            if is_pick == True and is_deliver==False:
                state = "picked"
            elif is_pick == True and is_deliver == True:
                state = "delivered"
            else:
                state = "pending"

            info = {
                "order_id": i.id,
                "state": state,
                "seller_name": i.organization,
                "street_address": i.street_address,
                "Order_date": i.date.strftime("%y-%m-%d"),
                "net": i.net,
                "cus_id":i.cus_id

            }
            res.append(info)

        res = jsonify(res)
        res.status_code = HTTPStatus.CREATED
    except Exception as e:
        res = jsonify(status="fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    return res




## return
def create_return_order():
    pass

@token_required
def create_pickup_return(data):
    try:
        ord_id=data.get("order_id")
        res = {}
        order_r = db.session.query(OrderReturn).filter_by(order_id=ord_id).first()
        print(order_r)
        order_r.is_pick = True
        db.session.commit()
        

        res = jsonify(
            status="success",
            message="picked",
        )

    except Exception as e:
        res = jsonify(status="fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    return res


# one return order details

@token_required
def get_return_details(ord_id):
   
    try:

        deliverer_id = get_return_details.user_id
        res = []
        # roduct_details=0
        state = ""       

        return_orders = (
            db.session.query(
                OrderReturn.id.label('return_id'),
                OrderReturn.ref_no,
                OrderReturn.date,
                OrderReturn.note,                
                OrderReturn.is_pick,
                OrderReturn.is_deliver,
                OrderReturn.order_id,
                OrderMobile.order_id,
                Order.id.label('order_id'),
                OrderMobile.cus_id,
                Order.seller_prof,                
            )
            #.join(Order,Order.id == OrderMobile.order_id)
            .join(Order,OrderReturn.order_id == Order.id)
            .join(OrderMobile,OrderMobile.order_id == Order.id)                      
            .filter(OrderReturn.deliverer_id == deliverer_id, OrderReturn.order_id == ord_id)
            .first()
        )
        print(return_orders.return_id)     



        # get customer details
        cus_q = (
            db.session.query(
                CustomerUser.id.label("cus_id"),
                CustomerUser.contact_no,
                CustomerProfile.ref_no,
                OrderMobile.order_id,
            )
            .join(OrderMobile, OrderMobile.cus_id == CustomerUser.id)
            .join(CustomerProfile, CustomerProfile.cus_id == CustomerUser.id)
            .filter(CustomerUser.id == return_orders.cus_id)
            .first()
        )

        print(cus_q)

        # seller details
        seller_q = (
            db.session.query(
                SellerUser.id.label("seller_id"),
                SellerProfile.first_name,
                SellerProfile.contact_no,
                SellerProfile.organization,
                SellerProfile.ref_no,
                Order.id,
            )
            .join(SellerProfile, SellerProfile.seller_id == SellerUser.id)
            .join(Order,Order.seller_prof==SellerProfile.seller_id)
            .filter(SellerProfile.id == return_orders.seller_prof)
            .first()
        )

        
        if return_orders:
                    # order State
            i=return_orders
            is_pick= i.is_pick           
            is_deliver = i.is_deliver
            if is_pick == True and is_deliver==False:
                state = "picked"
            elif is_deliver == True:
                state = "delivered"
            else:
                state = "pending"

            info = {
                "return_id": i.return_id,
                "order_id":i.order_id,
                "ref_no": i.ref_no,
                "date": i.date.strftime("%y-%m-%d"),
                "state": state,
                "note": i.note,
                "Customer_ref_no": cus_q.ref_no,
                "Customer_contact_no": cus_q.contact_no,
                "seller_ref": seller_q.ref_no,
                "Sellet_contact_no": seller_q.contact_no,
                
            }
            
            res.append(info)

            product_details = (
                db.session.query(
                    OrderReturnGrocery.grocery_order_id,
                    OrderReturnGrocery.qty,
                    GroceryProduct.name,
                )
                .join(
                    OrderGrocery, OrderGrocery.id == OrderReturnGrocery.grocery_order_id
                )
                .join(GroceryProduct, GroceryProduct.id == OrderGrocery.product_id)
                .filter(OrderReturnGrocery.return_id == i.return_id)
                .all()
            )
            print(product_details)
            
            for x in product_details:
                info2 = {
                    "grocery_order_id": x.grocery_order_id,
                    "qty": x.qty,
                    "product_name": x.name,
                }
                res.append(info2)
        res = jsonify(res)
        res.status_code = HTTPStatus.OK
    except Exception as e:
        res = jsonify(status="fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    return res




def create_return_deliver():
    pass

@token_required
def get_return_list():
    try:
        deliverer_id = get_return_list.user_id
        res = []
        print(deliverer_id)

        return_orders = (
            db.session.query(OrderReturn,OrderMobile,Order.id)
            .join(Order, Order.id == OrderReturn.order_id)
            .join(OrderMobile, OrderMobile.order_id == Order.id)
            .filter(OrderReturn.deliverer_id == deliverer_id)
            .all()
        )
        #print(return_orders)

        for i in return_orders:
            is_complete = i.OrderReturn.is_complete
            if is_complete == True:
                is_complete = "complete"
            else:
                is_complete = ""

            info = {
                "return_id": i.OrderReturn.id,
                "order_id":i.OrderReturn.order_id,
                "ref_no": i.OrderReturn.ref_no,
                "date": i.OrderReturn.date.strftime("%y-%m-%d"),
                "is_complete": is_complete,
            }
            res.append(info)

        res = jsonify(res)
        res.status_code = HTTPStatus.OK
    except Exception as e:
        res = jsonify(status="fail", message=str(e))
        res.status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    return res

    
