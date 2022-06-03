from core.http_api_provider import HttpApiProvider
from core.whales_provider import WhalesApiProvider
from core.liteclient_provider import LiteclientProvider


class ApiProviderFactory:
    @staticmethod
    def create(config):
        provider_name = config['current']
        provider_config = config[provider_name]

        if provider_name == 'http_api_provider':
            return HttpApiProvider(**provider_config)

        if provider_name == 'whales_provider':
            return WhalesApiProvider(**provider_config)

        if provider_name == 'liteclient_provider':
            return LiteclientProvider(**provider_config)

        raise Exception(f'Unknown provider name {provider_name}')
