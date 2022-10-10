from flask_restx.reqparse import RequestParser


#
# 
#--------------------------------------------- Request parsers----------------------------------

#
order_id_parser=RequestParser(bundle_errors=True)
order_id_parser.add_argument('order_id',type=int,location='json',required=True, nullable=False, help="order id int")








