from services.label_service import LabelService
from quart import Blueprint

from framework.handlers.response_handler_async import response_handler
from framework.logger.providers import get_logger
from framework.auth.wrappers.azure_ad_wrappers import azure_ad_authorization


logger = get_logger(__name__)
label_bp = Blueprint('label_bp', __name__)


@label_bp.route('/api/shipments/<shipment_id>/label', methods=['GET'], endpoint='get_label')
@response_handler
@azure_ad_authorization(scheme='read')
async def get_label(container, shipment_id: str):
    label_service: LabelService = container.resolve(
        LabelService)

    logger.info(f'Get label for shipment: {shipment_id}')
    label = await label_service.get_label(
        shipment_id=shipment_id)

    return {'label': label}


@label_bp.route('/api/shipments/<shipment_id>/label', methods=['POST'], endpoint='create_label')
@response_handler
@azure_ad_authorization(scheme='write')
async def create_label(container, shipment_id):
    label_service: LabelService = container.resolve(
        LabelService)

    logger.info(f'Create label for shipment: {shipment_id}')

    label = await label_service.create_label(
        shipment_id=shipment_id)

    return {'label': label}
