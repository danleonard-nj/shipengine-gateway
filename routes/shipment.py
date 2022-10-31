from models.requests import GetShipmentRequest
from services.shipment_service import ShipmentService
from quart import Blueprint, request

from framework.handlers.response_handler_async import response_handler
from framework.logger.providers import get_logger
from framework.auth.wrappers.azure_ad_wrappers import azure_ad_authorization
from framework.serialization.utilities import serialize


logger = get_logger(__name__)
shipment_bp = Blueprint('shipment_bp', __name__)


@shipment_bp.route('/api/shipment', methods=['GET'], endpoint='get_shipments')
@response_handler
@azure_ad_authorization(scheme='read')
async def get_shipment(container):
    shipment_service: ShipmentService = container.resolve(
        ShipmentService)

    _request = GetShipmentRequest(
        request=request)

    logger.info(f'Get shipments: {_request.to_json()}')

    shipments = await shipment_service.get_shipments(
        request=_request)

    return shipments


@shipment_bp.route('/api/shipment/<shipment_id>', methods=['GET'], endpoint='get_shipment')
@response_handler
@azure_ad_authorization(scheme='read')
async def get_shipment(container, shipment_id):
    shipment_service: ShipmentService = container.resolve(
        ShipmentService)

    shipment = await shipment_service.get_shipment(
        shipment_id=shipment_id)

    return shipment


@shipment_bp.route('/api/shipment', methods=['POST'], endpoint='post_shipment')
@response_handler
@azure_ad_authorization(scheme='write')
async def post_shipment(container):
    shipment_service: ShipmentService = container.resolve(
        ShipmentService)

    _content = await request.get_json()

    if not _content:
        raise Exception('Request body cannot be null')

    logger.info(f'Create shipment: {serialize(_content)}')
    result = await shipment_service.create_shipment(
        data=_content)

    return result


@shipment_bp.route('/api/shipment/<shipment_id>/cancel', methods=['PUT'], endpoint='cancel_shipment')
@response_handler
@azure_ad_authorization(scheme='write')
async def cancel_shipment(container, shipment_id: str):
    shipment_service: ShipmentService = container.resolve(
        ShipmentService)

    result = await shipment_service.cancel_shipment(
        shipment_id=shipment_id)
    return result
