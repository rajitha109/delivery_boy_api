from http import HTTPStatus
from flask_restx import Namespace, Resource

from .dto import bank_parser, bank_model, deposite_parser, withdraw_parser
from .functions import (
    delete_bank_details,
    save_bank_details,
    get_bank_details,
    update_bank_details,
    get_cash_in_hand,
    get_cash_in_hand,
    deposite_cash_in_hand,
    get_deposited_list,
    create_withdrawal_request,
    get_arrears_list,
    get_withdrawal_list,
    create_withdrawal_receive
)


finance_ns = Namespace(name="finance", validate=True)

finance_ns.models[bank_model.name] = bank_model

# bank details
@finance_ns.route("/bank", endpoint="bank")
class BankDetails(Resource):
    @finance_ns.doc(security="Bearer")
    @finance_ns.expect(bank_parser)
    @finance_ns.response(int(HTTPStatus.CREATED), "save bank data")
    @finance_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @finance_ns.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error."
    )
    # @finance_ns.marshal_with(bank_model)
    def post(self):
        """Save Bank Details"""
        data = bank_parser.parse_args()
        return save_bank_details(data)

    @finance_ns.doc(security="Bearer")
    @finance_ns.marshal_with(bank_model)
    @finance_ns.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error."
    )
    def get(self):
        """Get bank details"""
        return get_bank_details()

    @finance_ns.doc(security="Bearer")
    def delete(self):
        """Delete Data"""
        return delete_bank_details()

    @finance_ns.doc(security="Bearer")
    @finance_ns.expect(bank_parser)
    @finance_ns.response(int(HTTPStatus.CREATED), "update bank data")
    @finance_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @finance_ns.response(
        int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error."
    )
    def put(self):
        """update bank details"""
        data = bank_parser.parse_args()
        return update_bank_details(data)


# cash in hand
# @finance_ns.route("/cash",endpoint="cash_in_hand")
# class CashHand(Resource):
#    #@finance_ns.response(int(HTTPStatus.CREATED), "save bank data")
#    @finance_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
#    @finance_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
#    def post(self):
#        pass
#    def get(self):
#        pass


# Get cash in Hand list
@finance_ns.route("/cash", endpoint="cash_in_hand_list")
class CashInHand(Resource):
    """Handles HTTP requests to URL: /api/v1/finance/cash/list"""

    @finance_ns.doc(security="Bearer")
    @finance_ns.response(int(HTTPStatus.OK), "Query Run Successfully")
    @finance_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error")
    def get(self):
        """get all cash in hand list"""
        return get_cash_in_hand()


# deposite cash
@finance_ns.route("/deposite", endpoint="deposite_cih")
class Deposite(Resource):
    """Handles HTTP requests to URL: /api/v1/finance/deposite"""

    @finance_ns.doc(security="Bearer")
    @finance_ns.response(int(HTTPStatus.OK), "Query Run Successfully")
    @finance_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error")
    def get(self):
        """get all deposited list"""
        return get_deposited_list()

    @finance_ns.expect(deposite_parser)
    @finance_ns.doc(security="Bearer")
    @finance_ns.response(int(HTTPStatus.CREATED), "deposite cash in hand")
    @finance_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error")
    def post(self):
        """Deposite cash in hand

        Demo pass values
        {
        "cash_in_hand_list": "{'1':{'order_id':'pay_id'},'2':{'order_id':'pay_id'}}",
        "transaction_no": "1234"

        }

        Intended Result
        {
            status:success/fail,
            message:deposite,

        }
        """
        data = deposite_parser.parse_args()
        return deposite_cash_in_hand(data)


@finance_ns.route("/withdraw", endpoint="withdrawal_request")
class Withdrawa(Resource):
    """Handles HTTP requests to URL: /api/v1/finance/withdraw"""

    @finance_ns.expect(withdraw_parser)
    @finance_ns.doc(security="Bearer")
    @finance_ns.response(int(HTTPStatus.CREATED), "withdraw")
    @finance_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error")
    def post(self):
        """withdraw

        Demo pass values
        {
        "withdraw_list": "{'1':{'order_id':'pay_id'},'2':{'order_id':'pay_id'}}",
        "withdraw_amount": "",


        }

        Intended Result
        {
            status:success/fail,
            message:deposite,

        }
        """
        data = withdraw_parser.parse_args()
        return create_withdrawal_request(data)

    @finance_ns.doc(security="Bearer")    
    @finance_ns.response(int(HTTPStatus.OK), "Query success")
    @finance_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error")
    def get(self):
        """get withdrawal request list"""
        return get_withdrawal_list()



    """ Handles HTTP requests to URL: /api/v1/finance/withdraw/list"""
@finance_ns.route("/arrears/list", endpoint="arrears_list")
class Arrears(Resource):
    """Handles HTTP requests to URL: /api/v1/finance/arrears/list"""

    
    @finance_ns.doc(security="Bearer")    
    @finance_ns.response(int(HTTPStatus.OK), "Query success")
    @finance_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error")
    def get(self):
        """get all arrears list"""
        return get_arrears_list()




@finance_ns.route("/withdraw/receive", endpoint="withdrawal_receive")
class WithdrawaReceive(Resource):
    """Handles HTTP requests to URL: /api/v1/finance/withdraw/receive"""

    @finance_ns.doc(security="Bearer")
    @finance_ns.response(int(HTTPStatus.CREATED), "withdraw")
    @finance_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error")
    def post(self):
        """withdraw receive action        

        Intended Result
        {
            status:success,            

        }
        """        
        return create_withdrawal_receive()