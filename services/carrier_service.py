from typing import Dict, List

from clients.shipengine_client import ShipEngineClient
from constants.cache import CacheKey
from framework.clients.cache_client import CacheClientAsync
from framework.clients.http_client import HttpClient
from framework.logger.providers import get_logger
from models.carrier import Carrier, CarrierServiceModel

from services.shipengine_base import ShipEngineBase

logger = get_logger(__name__)


class CarrierService(ShipEngineBase):
    def __init__(
        self,
        shipengine_client: ShipEngineClient,
        cache_client: CacheClientAsync
    ):
        self.__client = shipengine_client
        self.__cache_client = cache_client
        self.__http_client = HttpClient()

    async def __get_carriers(
        self
    ) -> List[Dict]:
        cached_carriers = await self.__cache_client.get_json(
            key=CacheKey.CARRIER_LIST)

        if cached_carriers is not None:
            logger.info('Returning carriers from cache')
            return cached_carriers

        logger.info(f'Fetching carriers from client')
        response = await self.__client.get_carriers()
        carriers = response.get('carriers')

        await self.__cache_client.set_json(
            key=CacheKey.CARRIER_LIST,
            value=carriers,
            ttl=60 * 24 * 7)

        return carriers

    async def get_carrier_models(
        self
    ) -> List[Carrier]:
        logger.info('Parsing carrier models from carrier repsonse')
        carriers = await self.__get_carriers()

        return [
            Carrier(data=carrier)
            for carrier in carriers
        ]

    async def get_carriers(
        self
    ) -> Dict:
        logger.info('Get carrier list from ShipEngine')

        models = await self.get_carrier_models()
        return [model.to_json() for model in models]

    def __parse_carriers_response(
        self,
        carriers
    ):
        if not carriers:
            raise Exception(f'Failed to fetch carriers from ShipEngine')

        results = []
        for carrier in carriers:
            model = Carrier(data=carrier)
            results.append(model.to_json())

        return {
            'carriers': results
        }

    async def get_service_codes(
        self
    ) -> Dict:
        logger.info('Get service codes')

        response = await self.__client.get_carriers()
        carriers = response.get('carriers')

        results = []
        for carrier in carriers:
            services = carrier.get('services')
            if services:
                for service in services:
                    model = CarrierServiceModel(data=service)
                    results.append(model.to_json())

        return {
            'service_codes': results
        }

    async def get_balances(
        self
    ):
        logger.info('Get carrier balances')

        response = await self.__client.get_carriers()
        carriers = response.get('carriers')

        results = []
        for carrier in carriers:
            model = Carrier(data=carrier)

            results.append({
                'carrier_id': model.carrier_id,
                'carrier_code': model.carrier_code,
                'carrier_name': model.name,
                'balance': model.balance
            })

        return {
            'balances': results
        }
