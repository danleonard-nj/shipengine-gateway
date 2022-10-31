from clients.shipengine_client import ShipEngineClient
from framework.abstractions.abstract_request import RequestContextProvider
from framework.auth.azure import AzureAd
from framework.auth.configuration import AzureAdConfiguration
from framework.clients.cache_client import CacheClientAsync
from framework.configuration.configuration import Configuration
from framework.di.service_collection import ServiceCollection
from framework.di.static_provider import ProviderBase
from quart import Quart, request
from services.carrier_service import CarrierService
from services.label_service import LabelService
from services.mapper_service import MapperService
from services.rate_service import RateService
from services.shipment_service import ShipmentService


class AdRole:
    READ = 'ShipEngine.Read'
    WRITE = 'ShipEngine.Write'


def configure_azure_ad(container):
    configuration = container.resolve(Configuration)

    # Hook the Azure AD auth config into the service
    # configuration
    ad_auth: AzureAdConfiguration = configuration.ad_auth
    azure_ad = AzureAd(
        tenant=ad_auth.tenant_id,
        audiences=ad_auth.audiences,
        issuer=ad_auth.issuer)

    azure_ad.add_authorization_policy(
        name='read',
        func=lambda t: AdRole.READ in t.get('roles'))

    azure_ad.add_authorization_policy(
        name='write',
        func=lambda t: AdRole.WRITE in t.get('roles'))

    return azure_ad


class ContainerProvider(ProviderBase):
    @classmethod
    def configure_container(cls):
        container = ServiceCollection()

        container.add_singleton(Configuration)
        container.add_singleton(CacheClientAsync)

        container.add_singleton(
            dependency_type=AzureAd,
            factory=configure_azure_ad)

        container.add_singleton(MapperService)
        container.add_singleton(ShipEngineClient)
        container.add_singleton(CarrierService)

        container.add_transient(LabelService)
        container.add_transient(RateService)
        container.add_transient(ShipmentService)

        return container


def add_container_hook(app: Quart):
    def inject_container():
        RequestContextProvider.initialize_provider(
            app=app)
        if request.view_args != None:
            request.view_args['container'] = ContainerProvider.get_container()

    app.before_request_funcs.setdefault(
        None, []).append(
            inject_container)
