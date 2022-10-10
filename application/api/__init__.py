from flask import Blueprint
from flask_restx import Api

from application.api.user.endpoints import user_ns
from application.api.finance.endpoints import finance_ns
from application.api.sale.endpoints import sale_ns
from application.api.performance.endpoints import performance_ns


api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(
    api_bp,
    version="1.0",
    title="GoGett Delivery Boy App",
    description="GoGett Grocery and Food Delivery Boy App API.",
    doc='/ui',
    authorizations=authorizations,
)

# Namespaces

api.add_namespace(user_ns, path="/user")
api.add_namespace(finance_ns, path="/finance")
api.add_namespace(sale_ns, path="/sale")
api.add_namespace(performance_ns, path="/performance")