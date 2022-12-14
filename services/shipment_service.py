from typing import Dict

from clients.shipengine_client import ShipEngineClient
from framework.clients.cache_client import CacheClientAsync
from framework.logger.providers import get_logger
from framework.serialization.utilities import serialize
from models.requests import GetShipmentRequest
from models.shipment import CreateShipment, Shipment
from utilities.utils import first_or_default

from services.mapper_service import MapperService

logger = get_logger(__name__)


class ShipmentService:
    def __init__(
        self,
        mapper_service: MapperService,
        shipengine_client: ShipEngineClient
    ):
        self.__mapper_service = mapper_service
        self.__client = shipengine_client

    async def cancel_shipment(
        self,
        shipment_id: str
    ) -> Dict:
        logger.info(f'Cancel shipment: {shipment_id}')

        await self.__client.cancel_shipment(
            shipment_id=shipment_id)

        return {
            'deleted': True
        }

    async def get_shipments(
        self,
        request: GetShipmentRequest
    ) -> Dict:
        logger.info('Get shipments from ShipEngine client')

        response = await self.__client.get_shipments(
            page_number=request.page_number,
            page_size=request.page_size)

        logger.info('Shipments fetched successfully')

        service_code_mapping = await self.__mapper_service.get_carrier_service_code_mapping()
        carrier_mapping = await self.__mapper_service.get_carrier_mapping()

        shipments = []
        for shipment in response.get('shipments'):
            model = Shipment(
                data=shipment,
                service_code_mapping=service_code_mapping,
                carrier_mapping=carrier_mapping)
            shipments.append(model.to_json())

        return {
            'shipments': shipments,
            'page_number': response.get('page'),
            'total_pages': response.get('pages'),
            'result_count': response.get('total')
        }

    async def create_shipment(
        self,
        data: Dict
    ) -> Dict:
        shipment = CreateShipment(
            data=data)

        shipment_data = shipment.to_json()

        result = await self.__client.create_shipment(
            data=shipment_data)

        created = first_or_default(result.get('shipments'))
        logger.info(f'Response: {serialize(created)}')

        if not created:
            raise Exception('No response content returned from client')

        logger.info('Parsing created shipment model')
        created_shipment = Shipment(
            data=created)

        return {
            'shipment_id': created_shipment.shipment_id
        }

    async def update_shipment(
        self,
        data: Dict
    ) -> Dict:
        shipment = CreateShipment(
            data=data)

        shipment_data = shipment.to_json()

        result = await self.__client.create_shipment(
            data=shipment_data)

        created = first_or_default(result.get('shipments'))
        logger.info(f'Response: {serialize(created)}')

        if not created:
            raise Exception('No response content returned from client')

        logger.info('Parsing created shipment model')
        created_shipment = Shipment(
            data=created)

        return {
            'shipment_id': created_shipment.shipment_id
        }

    async def get_shipment(
        self,
        shipment_id
    ):
        logger.info(f'Get shipment: {shipment_id}')
        shipment = await self.__client.get_shipment(
            shipment_id=shipment_id)

        logger.info(f'Fetching carrier mapping')
        service_code_mapping = await self.__mapper_service.get_carrier_service_code_mapping()
        carrier_mapping = await self.__mapper_service.get_carrier_mapping()

        result = Shipment(
            data=shipment,
            service_code_mapping=service_code_mapping,
            carrier_mapping=carrier_mapping)

        return result.to_json()
