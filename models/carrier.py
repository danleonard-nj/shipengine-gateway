from services.fields import Field, FieldClass


class CarrierServiceModel:
    def __init__(self, data):
        self.service_code = data.get('service_code')
        self.name = data.get('name')

    def to_json(self):
        return {
            'service_code': self.service_code,
            'name': self.name
        }


class Carrier:
    def __init__(self, data):
        self.carrier_id = data.get('carrier_id')
        self.carrier_code = data.get('carrier_code')
        self.name = data.get('friendly_name')
        self.account_number = data.get('account_number')
        self.balance = data.get('balance')
        self.services = [CarrierServiceModel(data=service)
                         for service in data.get('services')
                         if data.get('services') is not None]

    def to_json(self):
        return {
            'carrier_id': self.carrier_id,
            'carrier_code': self.carrier_code,
            'name': self.name,
            'account_number': self.account_number,
            'balance': self.balance,
            'services': [x.to_json() for x
                         in self.services]
        }
