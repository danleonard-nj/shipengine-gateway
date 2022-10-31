
from datetime import datetime
from typing import Dict

from clients.shipengine_client import ShipEngineClient
from dateutil import parser
from framework.logger.providers import get_logger
from framework.serialization.utilities import serialize
from framework.validators.nulls import not_none
from models.label import Label
from utilities.utils import first_or_default

from services.shipengine_base import ShipEngineBase

logger = get_logger(__name__)


class LabelService:
    def __init__(
        self,
        shipengine_client: ShipEngineClient
    ):
        self.__client = shipengine_client

    async def create_label(
        self,
        shipment_id: str
    ):
        not_none(shipment_id, 'shipment_id')

        logger.info(f'Create label from shipment: {shipment_id}')

        # Fetch the shipment and update the ship date if it's not current.  The API
        # doesn't provide any capabilities to do this on the fly when requesting the
        # label, so if the ship date is in the past it'll just error out
        shipment = await self.__client.get_shipment(
            shipment_id=shipment_id)

        if shipment is None:
            raise Exception(f"No shipment with the ID '{shipment_id}' exists")

        ship_date = parser.parse(shipment.get('ship_date'))
        logger.info(f'Ship date: {ship_date.isoformat()}')

        now = datetime.now()
        if ship_date.date() != now.date():
            logger.info(f'Updating ship date to {now.date()}')

            shipment['ship_date'] = now.date().isoformat()

            logger.info(f'Sending shipment update call')
            update_response = await self.__client.update_shipment(
                shipment_id=shipment_id,
                data=shipment)

            logger.info(f'Update response: {serialize(update_response)}')

        label = await self.__client.create_label(
            shipment_id=shipment_id)

        logger.info(f'Response: {serialize(label)}')

        errors = label.get('errors') or []
        if len(errors) > 0:
            error_messages = [x.get('message') for x in errors]
            raise Exception(f'Error: {error_messages}')

        return label

    async def get_label(
        self,
        shipment_id: str
    ) -> Dict:
        logger.info(f'Get label for shipment: {shipment_id}')
        not_none(shipment_id, 'shipment_id')

        label_response = await self.__client.get_label(
            shipment_id=shipment_id)

        label = first_or_default(
            label_response.get('labels'))

        if label is None:
            return {
                'label': None
            }

        model = Label(
            data=label)

        return model.to_json()
