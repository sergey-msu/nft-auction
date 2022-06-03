import sys
import yaml
import time
from pprint import pprint

from core.builder import Builder
from core.api_provider_factory import ApiProviderFactory
from contracts.snft_provider import SnftProvider
from contracts.snft_request import SnftRequest


def main():
    with open('configs/app.yaml') as f:
        config = yaml.safe_load(f)

    builder = Builder(**config['core'])
    api = ApiProviderFactory.create(config['api'])

    builder.clear_out()
    builder.compile_sources(**config['compile'])
    builder.build_templates(**config['compile'])

    sign_provider = SnftProvider(builder, api, 
                                 address=config['core']['sign_provider_address'],
                                 pk_file=config['core']['sign_provider_pk'],
                                 user=7)

    send = bool(int(sys.argv[1]))
    sign_provider.cancel_sign_request(object_address='EQAOiZWI0ylAIrYahIblh-g3ph14Qp5Gy0AnjpMS72ewxMqZ',
                                      signee_address='EQB1grTB2NIAbshA8C1Fu8EiSHiY_ZbTE-tRneTMKgdHAUJH',
                                      deploy_request_ng=15_000_000,
                                      send=send)

    if not send:
        # TODO: address = collection.get_request_address_by_signee(...)
        sign = SnftRequest(builder, api, address='kQAjyqud2iNeY-MN-LjFG5J3qHtgfK2CCxdN4wfN77Avw0nu')
        print('state:', sign.state(True))
        print('balance:', sign.balance(True))


if __name__ == '__main__':
    main()
