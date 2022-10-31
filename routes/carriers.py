from services.carrier_service import CarrierService
from quart import Blueprint

from framework.handlers.response_handler_async import response_handler
from framework.logger.providers import get_logger
from framework.auth.wrappers.azure_ad_wrappers import azure_ad_authorization

logger = get_logger(__name__)
carrier_bp = Blueprint('carrier_bp', __name__)


@carrier_bp.route('/api/carriers', methods=['GET'], endpoint='get_carriers')
@response_handler
@azure_ad_authorization(scheme='read')
async def get_carriers(container):
    carrier_service: CarrierService = container.resolve(
        CarrierService)

    response = await carrier_service.get_carriers()
    return {'carriers': response}


@carrier_bp.route('/api/carriers/balances', methods=['GET'], endpoint='get_balances')
@response_handler
@azure_ad_authorization(scheme='read')
async def get_balances(container):
    carrier_service: CarrierService = container.resolve(
        CarrierService)

    response = await carrier_service.get_balances()
    return response


@carrier_bp.route('/api/carriers/services', methods=['GET'], endpoint='get_service_codes')
@response_handler
@azure_ad_authorization(scheme='read')
async def get_service_codes(container):
    carrier_service: CarrierService = container.resolve(
        CarrierService)

    response = await carrier_service.get_service_codes()
    return response
