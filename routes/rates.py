from services.rate_service import RateService
from quart import Blueprint, request

from framework.handlers.response_handler_async import response_handler
from framework.logger.providers import get_logger
from framework.auth.wrappers.azure_ad_wrappers import azure_ad_authorization

logger = get_logger(__name__)
rates_bp = Blueprint('rates_bp', __name__)


@rates_bp.route('/api/rates', methods=['POST'], endpoint='get_rates')
@response_handler
@azure_ad_authorization(scheme='read')
async def get_rates(container):
    rate_service: RateService = container.resolve(
        RateService)

    data = await request.get_json()
    response = await rate_service.get_rates(
        shipment=data)

    return response
