
from typing_extensions import Required
from flask_restx import Model
from flask_restx.reqparse import RequestParser



#-------------------------------Request Parsers---------------------------------------------------#

# Customer Ticket
ticket_parser = RequestParser(bundle_errors=True)
ticket_parser.add_argument(
    "ticket_category_id",
    type=int,
    location="json",
    required=False,
    nullable=True,
    help="ticket category",
)
ticket_parser.add_argument(
    "customer_text",
    type=str,
    location="json",
    required=False,
    nullable=True,
    help="string ticket message",
)



# Use on seller review_create
seller_rev_parser = RequestParser(bundle_errors=True)
seller_rev_parser.add_argument("seller_id",type=int,location="json",required=True,nullable=False,help="seller id")
seller_rev_parser.add_argument('rate', type=int, location="json", required=True, nullable=False, help="int 1 to 5 ")
seller_rev_parser.add_argument('review',type=str, location="json", required=False, nullable=True,help="review as string(255)")
seller_rev_parser.add_argument("order_id",type=int,location="json",required=True,nullable=False,help="order id")

# Use on customer review_create
customer_rev_parser = RequestParser(bundle_errors=True)
customer_rev_parser.add_argument("customer_id",type=int,location="json",required=True,nullable=False,help="customer id")
customer_rev_parser.add_argument('rate', type=int, location="json", required=True, nullable=False, help="int 1 to 5 ")
customer_rev_parser.add_argument('review',type=str, location="json", required=False, nullable=True,help="review as string(255)")
customer_rev_parser.add_argument("order_id",type=int,location="json",required=True,nullable=False,help="order id")