from http import HTTPStatus
from flask_restx import Namespace, Resource

from .dto import ticket_parser, seller_rev_parser, customer_rev_parser

from .functions import (
    deliver_ticket_create,
    get_customer_review,
    seller_review_create,
    customer_review_create,
    get_completed_list,
    get_failed_list,
    get_customer_review,
    get_seller_review
)

performance_ns = Namespace(name="performance", validate=True)


# completed orders
@performance_ns.route("/completed/list", endpoint="completed_list")
class CompletedList(Resource):
    """Handles HTTP requests to URL: /api/v1/perfomance/completed/list"""

    @performance_ns.doc(security="Bearer")
    @performance_ns.response(int(HTTPStatus.OK), "Query Run Successfully")
    @performance_ns.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error"
    )
    def get(self):
        """get all completed orders"""

        return get_completed_list()


# Failed orders
@performance_ns.route("/failed/list", endpoint="failed_list")
class FailedList(Resource):
    """Handles HTTP requests to URL: /api/v1/perfomance/failed/list"""

    @performance_ns.doc(security="Bearer")
    @performance_ns.response(int(HTTPStatus.OK), "Query Run Successfully")
    @performance_ns.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error"
    )
    def get(self):
        """get all failed orders"""

        return get_failed_list()


# ratings and reviews seller
@performance_ns.route("/reviews/seller", endpoint="seller_reviews")
class SellerReview(Resource):
    """Handles HTTP requests to URL: /api/v1/performance/review/seller>"""

    @performance_ns.doc(security="Bearer")
    @performance_ns.expect(seller_rev_parser)
    @performance_ns.response(int(HTTPStatus.OK), "create review.")
    @performance_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @performance_ns.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error."
    )
    def post(self):
        """Post deliver-seller review
        Demo pass values
        { seller_id:int,rate:Integer ,review:String  }

        Intended Result
        {
            status:success/fail,
            message:review_created or error

        }
        """
        data = seller_rev_parser.parse_args()
        res = seller_review_create(data)

        return res

    """Handles HTTP requests to URL: /api/v1/performance/review/seller/list"""

    @performance_ns.doc(security="Bearer")
    @performance_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @performance_ns.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error."
    )
    def get(self):
        """Get seller reviews"""
        return get_seller_review()


# ratings and reviews customer
@performance_ns.route("/reviews/customer", endpoint="customer_reviews")
class CustomerReview(Resource):
    """Handles HTTP requests to URL: /api/v1/performance/review/customer"""

    @performance_ns.doc(security="Bearer")
    @performance_ns.expect(customer_rev_parser)
    @performance_ns.response(int(HTTPStatus.OK), "Profile saved.")
    @performance_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @performance_ns.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error."
    )
    def post(self):
        """Post deliver-customer review
        Demo pass values
        {  customer_id:Integer, rate:Integer ,review:String  }

        Intended Result
        {
            status:success/fail,
            message:review_created or error

        }
        """
        data = customer_rev_parser.parse_args()
        res = customer_review_create(data)

        return res

    """Handles HTTP requests to URL: /api/v1/performance/review/customer/list"""

    @performance_ns.doc(security="Bearer")
    @performance_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @performance_ns.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error."
    )
    def get(self):
        """Get Customer reviews"""
        return get_customer_review()


# ratings and reviews customer
#@performance_ns.route("/reviews/list", endpoint="list_reviews")
#class AllReviews(Resource):
#    """Handles HTTP requests to URL: /api/v1/performance/review/list"""

#    @performance_ns.doc(security="Bearer")
#    @performance_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
#    @performance_ns.response(
#        int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error."
#    )
#    def get(self):
#        """All reviews"""
#        pass


# deliver Ticket
@performance_ns.route("/ticket", endpoint="deliver_ticket_create")
class CustomerTicket(Resource):
    @performance_ns.doc(security="Bearer")
    @performance_ns.expect(ticket_parser)
    @performance_ns.response(int(HTTPStatus.OK), "Customer Ticket")
    @performance_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    def post(self):
        """Post customer Ticket
        Demo pass values
        { ticket_category_id:1,
        customer_text:str ,

          }

        Intended Result
        {
            status:success/fail,
            message:

        }
        """
        data = ticket_parser.parse_args()
        res = deliver_ticket_create(data)
        return res

    @performance_ns.response(int(HTTPStatus.OK), "Query Run Successfully")
    @performance_ns.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error"
    )
    def get(self):
        """get ticket categories"""

        pass


# deliver Ticket
@performance_ns.route("/update/<int:ticket_id>", endpoint="deliver_ticket_update")
class UpdateTicket(Resource):
    @performance_ns.response(int(HTTPStatus.OK), "Query Run Successfully")
    @performance_ns.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error"
    )
    def put(self, ticket_id):
        """Update ticket status"""

        pass
