

from typing import Coroutine
from services.carrier_service import CarrierService
from services.shipengine_base import ShipEngineBase
from models.rate import Rate, ShipmentRate

from framework.logger.providers import get_logger
from framework.serialization.utilities import serialize

logger = get_logger(__name__)


class RateService(ShipEngineBase):
    def __init__(self, container):
        super().__init__(container)

        self.carrier_service: CarrierService = container.resolve(
            CarrierService)

    async def get_rates(self, shipment: dict) -> dict:
        logger.info('Get shipment rates')

        carriers = await self.carrier_service.get_carriers()
        carrier_ids = [
            x.get('carrier_id')
            for x in carriers
        ]

        logger.info(
            f'Carrier IDs to run rate against: {serialize(carrier_ids)}')

        model = ShipmentRate().from_json(
            data=shipment,
            carrier_ids=carrier_ids)
        model.validate()

        rate_request = model.to_shipment_json()
        rates = await self.client.get_rates(
            shipment=rate_request)

        rate_response = rates.get('rate_response')
        rate_details = rate_response.get('rates')

        carrier_rate_errors = {
            error.get('carrier_id'): self.to_rate_error(error)
            for error in rate_response.get('errors')
        }

        results = [
            Rate(rate, carrier_rate_errors).to_rate()
            for rate in rate_details
        ]

        carrier_rates = {}
        for rate in results:
            carrier_id = rate.get('carrier').get('carrier_id')
            if carrier_rates.get(carrier_id) is None:
                carrier_rates[carrier_id] = []

            carrier_rate = carrier_rates[carrier_id]
            carrier_rate.append(rate)
            carrier_rates[carrier_id] = carrier_rate

        return {
            'quotes': carrier_rates,
            'errors': carrier_rate_errors
        }

    def to_rate_error(self, error: dict) -> dict:
        return {
            "error_code": error.get('error_code'),
            "error_source": error.get('error_source'),
            "error_type": error.get('error_type'),
            "message": error.get('message')
        }
