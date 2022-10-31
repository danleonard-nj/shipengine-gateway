from quart import Quart
from routes.shipment import shipment_bp
from routes.carriers import carrier_bp
from routes.rates import rates_bp
from routes.labels import label_bp
from routes.health import health_bp
from dotenv import load_dotenv
from utilities.provider import add_container_hook

from framework.logger.providers import get_logger


load_dotenv()

logger = get_logger(__name__)

app = Quart(__name__)

app.register_blueprint(health_bp)
app.register_blueprint(shipment_bp)
app.register_blueprint(carrier_bp)
app.register_blueprint(rates_bp)
app.register_blueprint(label_bp)

add_container_hook(app)

if __name__ == '__main__':
    app.run(debug=True, port='5088')
