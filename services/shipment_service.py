

from typing import Coroutine
from models.requests import GetShipmentRequest
from models.shipment import Shipment, CreateShipment
from services.mapper_service import MapperService
from services.shipengine_base import ShipEngineBase
from utilities.utils import first_or_default

from framework.serialization.utilities import serialize
from framework.logger.providers import get_logger
from framework.clients.cache_client import CacheClientAsync

logger = get_logger(__name__)


class ShipmentService(ShipEngineBase):
    def __init__(self, container):
        super().__init__(container)

        self.cache_client = container.resolve(CacheClientAsync)
        self.mapper_service: MapperService = container.resolve(
            MapperService)

    async def cancel_shipment(self, shipment_id: str) -> dict:
        logger.info(f'Cancel shipment: {shipment_id}')

        response = await self.client.cancel_shipment(
            shipment_id=shipment_id)

        errors = response.get('errors') or []
        logger.info(f'Errors: {errors}')

        if len(errors) > 0:
            logger.info('Failed to cancel shipment')
            error_messages = [x.get('message') for x in errors]

            logger.info(error_messages)
            raise Exception(f'Failed to cancel shipment: {error_messages}')

        return response

    async def get_shipments(self, request: GetShipmentRequest) -> dict:
        logger.info('Get shipments from ShipEngine client')

        response = await self.client.get_shipments(
            page_number=request.page_number,
            page_size=request.page_size)

        logger.info('Shipments fetched successfully')

        service_code_mapping = await self.mapper_service.get_carrier_service_code_mapping()
        carrier_mapping = await self.mapper_service.get_carrier_mapping()

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

    async def create_shipment(self, data: dict) -> dict:
        shipment = CreateShipment(
            data=data)

        shipment_data = shipment.to_json()

        result = await self.client.create_shipment(
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

    async def update_shipment(self, data: dict) -> dict:
        shipment = CreateShipment(
            data=data)

        shipment_data = shipment.to_json()

        result = await self.client.create_shipment(
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

    async def get_shipment(self, shipment_id):
        logger.info(f'Get shipment: {shipment_id}')
        shipment = await self.client.get_shipment(
            shipment_id=shipment_id)

        logger.info(f'Fetching carrier mapping')
        service_code_mapping = await self.mapper_service.get_carrier_service_code_mapping()
        carrier_mapping = await self.mapper_service.get_carrier_mapping()

        result = Shipment(
            data=shipment,
            service_code_mapping=service_code_mapping,
            carrier_mapping=carrier_mapping)

        return result.to_json()
