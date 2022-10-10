from http import HTTPStatus
from flask_restx import Namespace, Resource


from .dto import (
    order_id_parser
)

from .functions import (
   
    create_pickup_order,
    get_order_details,
    create_order_deliver,    
    get_order_list,    
    create_pickup_return,
    get_return_details,
    create_return_deliver,
    get_return_details,
    get_return_list,  
    create_accept_order,




)


sale_ns = Namespace(name="sale", validate=True)

############################# order #######################################
# order accept
@sale_ns.route("/order/accept", endpoint="accept_order")
class AcceptOrder(Resource):
    """Handles HTTP requests to URL: /api/v1/sale/order/accept"""
    @sale_ns.doc(security="Bearer")
    @sale_ns.expect(order_id_parser)
    @sale_ns.response(int(HTTPStatus.CREATED), "save accept")
    @sale_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @sale_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """accept order"""
        data=order_id_parser.parse_args()
        res = create_accept_order(data)
        return res


# order pickup
@sale_ns.route("/order/pickup", endpoint="pickup_order")
class PickupOrder(Resource):
    """Handles HTTP requests to URL: /api/v1/sale/order/pickup"""

    @sale_ns.doc(security="Bearer")
    @sale_ns.expect(order_id_parser)    
    @sale_ns.response(int(HTTPStatus.CREATED), "save pick up")
    @sale_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @sale_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Save Pickup"""
        data=order_id_parser.parse_args()
        res = create_pickup_order(data)
        return res


# grocery order details
@sale_ns.route("/order/details/<int:order_id>", endpoint="grocery_order_details")
class OrderDetails(Resource):

    @sale_ns.doc(security="Bearer")
    @sale_ns.response(int(HTTPStatus.OK), "Query run sucessfuly")
    @sale_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def get(self,order_id):
        """Pick up Order details"""

        res = get_order_details(order_id)
        return res


# order delivered
@sale_ns.route("/order/deliver", endpoint="delivered_order")
class DeliverOrder(Resource):
    """Handles HTTP requests to URL: /api/v1/sale/order/deliver"""

    @sale_ns.doc(security="Bearer")
    @sale_ns.expect(order_id_parser)
    @sale_ns.response(int(HTTPStatus.CREATED), "order delivered ")
    @sale_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @sale_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Order Delivery"""
        data=order_id_parser.parse_args()
        res = create_order_deliver(data)
        return res



# order seller details
@sale_ns.route("/order/list", endpoint="order_list")
class OrderList(Resource):
    """Handles HTTP requests to URL: /api/v1/sale/order/list"""

    @sale_ns.doc(security="Bearer")
    @sale_ns.response(int(HTTPStatus.OK), "Query Run Successfully")
    @sale_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error")
    def get(self):
        """get all orders"""
        res = get_order_list()
        return res


########################################### return ###########################################

# order accept
@sale_ns.route("/return/accept", endpoint="return_accept")
class AcceptReturn(Resource):
    """Handles HTTP requests to URL: /api/v1/sale/return/accept"""

   
    @sale_ns.response(int(HTTPStatus.CREATED), "save pick up")
    @sale_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @sale_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """accept order"""       
        pass


# order pickup
@sale_ns.route("/return/pickup/", endpoint="return_pickup")
class PickReturn(Resource):
    """Handles HTTP requests to URL: /api/v1/sale/return/pickup"""

    @sale_ns.doc(security="Bearer")
    @sale_ns.expect(order_id_parser)
    @sale_ns.response(int(HTTPStatus.CREATED), "save return pick up")
    @sale_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @sale_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Save Return Pickup"""
        data=order_id_parser.parse_args()
        res = create_pickup_return(data)
        return res



# order delivered
@sale_ns.route("/return/deliver", endpoint="delivered_return")
class DeliverReturn(Resource):
    """Handles HTTP requests to URL: /api/v1/sale/return/deliver"""
    @sale_ns.expect(order_id_parser)
    @sale_ns.response(int(HTTPStatus.CREATED), "return delivered ")
    @sale_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @sale_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Order Delivery"""
        data=order_id_parser.parse_args()
        res = create_return_deliver(data)
        return res


# return details
@sale_ns.route("/return/details/<int:order_id>", endpoint="return_order")
class CustomerReturn(Resource):
    """Handles HTTP requests to URL: /api/v1/sale/return/details/<int:order_id>"""
    @sale_ns.doc(security="Bearer")
    @sale_ns.response(int(HTTPStatus.OK), "Query Run Successfully")
    @sale_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error")
    def get(self, order_id):
        """return details"""

        res = get_return_details(order_id)
        return res



# order seller details
@sale_ns.route("/return/list", endpoint="return_list")
class ReturnList(Resource):
    """Handles HTTP requests to URL: /api/v1/sale/return/list"""

    @sale_ns.doc(security="Bearer")
    @sale_ns.response(int(HTTPStatus.OK), "Query Run Successfully")
    @sale_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error")
    def get(self):
        """get all return orders"""
        res = get_return_list()
        return res


