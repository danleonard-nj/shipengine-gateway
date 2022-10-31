import json


class Serializable:
    def to_json(self):
        return json.dumps(self, indent=True, default=str)


class GetShipmentRequest(Serializable):
    def __init__(self, request):
        self.shipengine_model = request.args.get('shipengine_model') == 'true'
        self.page_number = request.args.get('page_number') or 1
        self.page_size = request.args.get('page_size') or 25
