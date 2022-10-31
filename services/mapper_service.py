

from typing import List
from models.carrier import Carrier
from services.carrier_service import CarrierService
from framework.logger.providers import get_logger

logger = get_logger(__name__)


class MappingKey:
    CARRIER_SERVICE_CODE = 'carrier-service-code'
    CARRIER = 'carrier'


class MapperService:
    def __init__(self, container):
        self._mapping = dict()

        self.carrier_service: CarrierService = container.resolve(
            CarrierService)

    async def get_carrier_service_code_mapping(self):
        if self._mapping.get(MappingKey.CARRIER_SERVICE_CODE) is None:
            logger.info(
                f'Initializing mapping: {MappingKey.CARRIER_SERVICE_CODE}')
            await self._create_carrier_service_code_mapping()
        return self._mapping[MappingKey.CARRIER_SERVICE_CODE]

    async def get_carrier_mapping(self):
        if self._mapping.get(MappingKey.CARRIER) is None:
            logger.info(
                f'Initializing mapping: {MappingKey.CARRIER}')
            await self._create_carrier_mapping()
        return self._mapping[MappingKey.CARRIER]

    async def _create_carrier_mapping(self):
        logger.info('Building carrier mapping')

        mapping = dict()
        carriers = await self.carrier_service.get_carrier_models()

        for carrier in carriers:
            mapping[carrier.carrier_id] = carrier

        self._mapping[MappingKey.CARRIER] = mapping

    async def _create_carrier_service_code_mapping(self) -> None:
        logger.info(f'Building carrier service code mapping')

        mapping = dict()
        carriers = await self.carrier_service.get_carrier_models()

        for carrier in carriers:
            logger.info(f'Mapping carrier: {carrier}')

            for service_code in carrier.services:
                logger.info(
                    f'Mapping service code: {service_code.service_code} -> {service_code.name}')
                mapping[service_code.service_code] = service_code.name

        self._mapping[MappingKey.CARRIER_SERVICE_CODE] = mapping
