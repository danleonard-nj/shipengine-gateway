from models.mapping import mapped_value, tracking_status_mapping, label_status_mapping


class Label:
    def __init__(self, data):
        self.label_id = data.get('label_id')
        self.shipment_id = data.get('shipment_id')
        self.carrier_code = data.get('carrier_code')
        self.carrier_id = data.get('carrier_id')
        self.service_code = data.get('service_code')
        self.ship_date = data.get('ship_date')
        self.created_date = data.get('created_at')
        self.insurance_cost = data.get('insurance_cost').get('amount')
        self.download_pdf = data.get('label_download').get('pdf')
        self.download_png = data.get('label_download').get('png')
        self.shipment_cost = data.get('shipment_cost').get('amount')
        self.status = mapped_value(
            mapping=label_status_mapping,
            value=data.get('status'))
        self.tracking_number = data.get('tracking_number')
        self.tracking_status = mapped_value(
            mapping=tracking_status_mapping,
            value=data.get('tracking_status'))
        self.tracking_url = self._get_tracking_url(
            tracking_number=data.get('tracking_number'))
        self.voided = data.get('voided')
        self.voided_date = data.get('voided_at')

    def _get_tracking_url(self, tracking_number):
        return f'https://wwwapps.ups.com/WebTracking/track?track=yes&trackNums={tracking_number}'

    def to_json(self):
        return self.__dict__
