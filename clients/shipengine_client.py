from typing import Dict

from framework.clients.http_client import HttpClient
from framework.configuration.configuration import Configuration
from framework.logger.providers import get_logger
from framework.serialization.utilities import serialize
from framework.utilities.url_utils import build_url

logger = get_logger(__name__)


class ShipEngineClient:
    def __init__(
        self,
        configuration: Configuration
    ):
        self.http_client = HttpClient()
        self.base_url = configuration.shipengine.get(
            'base_url')
        self.key = configuration.shipengine.get(
            'api_key')

    def __get_headers(self) -> dict:
        return {
            'Content-Type': 'application/json',
            'API-Key': self.key
        }

    async def create_label(
        self,
        shipment_id: str
    ) -> Dict:
        logger.info(f'Get label for shipment: {shipment_id}')

        response = await self.http_client.post(
            url=f'{self.base_url}/labels/shipment/{shipment_id}',
            headers=self.__get_headers(),
            timeout=None)

        content = response.json()
        logger.info(f'Response status: {response.status_code}')
        logger.info(f'Response: {serialize(content)}')

        return content

    async def get_label(
        self,
        shipment_id: str
    ) -> Dict:
        logger.info(f'Get label for shipment: {shipment_id}')

        url = build_url(f'{self.base_url}/labels',
                        shipment_id=shipment_id)

        response = await self.http_client.get(
            url=url,
            headers=self.__get_headers(),
            timeout=None)

        logger.info(f'Status: {response.status_code}')
        return response.json()

    async def get_shipments(
        self,
        page_number: int,
        page_size: int
    ) -> Dict:
        logger.info('Get Shipments')

        url = build_url(
            base=f'{self.base_url}/shipments',
            sort_by='created_at',
            sort_dir='desc',
            page=page_number,
            page_size=page_size)

        logger.info(f'URL: {url}')

        response = await self.http_client.get(
            url=url,
            headers=self.__get_headers(),
            timeout=None)

        logger.info(f'Response Code: {response.status_code}')
        return response.json()

    async def create_shipment(
        self,
        data: Dict
    ) -> Dict:
        logger.info('Create shipment')

        response = await self.http_client.post(
            url=f'{self.base_url}/shipments',
            headers=self.__get_headers(),
            json=data,
            timeout=None)

        content = response.json()
        logger.info(f'Response status: {response.status_code}')
        logger.info(f'Response: {serialize(content)}')

        return content

    async def update_shipment(
        self,
        shipment_id: str,
        data: Dict
    ) -> Dict:
        logger.info('Update shipment')

        response = await self.http_client.put(
            url=f'{self.base_url}/shipments/{shipment_id}',
            headers=self.__get_headers(),
            json=data,
            timeout=None)

        content = response.json()
        logger.info(f'Status: {response.status_code}')
        logger.info(f'Response status: {response.status_code}')

        return content

    async def get_carriers(
        self
    ) -> Dict:
        logger.info('Get carriers from client')

        response = await self.http_client.get(
            url=f'{self.base_url}/carriers',
            headers=self.__get_headers(),
            timeout=None)

        content = response.json()

        logger.info(f'Response status: {response.status_code}')
        logger.info(f'Response: {serialize(content)}')

        return content

    async def cancel_shipment(
        self,
        shipment_id: str
    ):
        logger.info(f'Cancel shipment: {shipment_id}')

        response = await self.http_client.put(
            url=f'{self.base_url}/shipments/{shipment_id}/cancel',
            headers=self.__get_headers(),
            timeout=None)

        logger.info(f'Response: {response.status_code}')

    async def get_shipment(
        self,
        shipment_id: str
    ) -> Dict:
        logger.info(f'Get shipment: {shipment_id}')

        response = await self.http_client.get(
            url=f'{self.base_url}/shipments/{shipment_id}',
            headers=self.__get_headers(),
            timeout=None)

        content = response.json()
        logger.info(f'Response status: {response.status_code}')
        logger.info(f'Response: {serialize(content)}')

        return content or dict()

    async def get_rates(
        self,
        shipment: Dict
    ) -> Dict:
        logger.info('Get rates')

        # TODO: Switch to estimate route /api/rates/estimate
        response = await self.http_client.post(
            url=f'{self.base_url}/rates',
            json=shipment,
            headers=self.__get_headers(),
            timeout=None)

        content = response.json()

        logger.info(f'Response code: {response.status_code}')
        logger.info(f'Response: {content}')

        return content
