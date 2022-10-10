from flask_restx import Model
from flask_restx.reqparse import RequestParser
from flask_restx.fields import String, Boolean, Integer, Float

bank_model=Model(
    'DeliveryBank',
    {
        'bank_name':String,
        'branch':String,
        'acc_no':String,
        'acc_holder':String,
    }
)




#
# ---------------------------------------Request parsers--------------------------------------------------------------------------


#bank details parser
bank_parser=RequestParser(bundle_errors=True)
bank_parser.add_argument('bank_name',type=str,location="json",required=True,nullable=False,help="Bank name")
bank_parser.add_argument('branch',type=str,location="json",required=True,nullable=False,help="bank branch")
bank_parser.add_argument('acc_no',type=str,location="json",required=True,nullable=False,help="account number")
bank_parser.add_argument('acc_holder',type=str,location="json",required=True,nullable=False,help="account holder")




deposite_parser=RequestParser(bundle_errors=True)
deposite_parser.add_argument('cash_in_hand_list',type=str,location="json",required=True,nullable=False,help="cash in hand list")
deposite_parser.add_argument('transaction_no',type=str,location='json',required=True, nullable=False, help="transaction_no str")


withdraw_parser=RequestParser(bundle_errors=True)
withdraw_parser.add_argument('withdraw_list',type=str,location="json",required=True,nullable=False,help="withdraw list")
withdraw_parser.add_argument('note',type=str,location="json",required=False,nullable=True,help="note")










