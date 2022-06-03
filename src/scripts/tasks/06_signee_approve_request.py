import sys
import yaml
import time
from pprint import pprint

from core.builder import Builder
from core.api_provider_factory import ApiProviderFactory
from contracts.snft_request import SnftRequest
from contracts.signee import Signee


def main():
    with open('configs/app.yaml') as f:
        config = yaml.safe_load(f)

    builder = Builder(**config['core'])
    api = ApiProviderFactory.create(config['api'])

    builder.clear_out()
    builder.compile_sources(**config['compile'])
    builder.build_templates(**config['compile'])

    signee = Signee(builder, api,
                    address='EQDaA6jKp9dwhESNfjBIVU54Pz8VJO4VUIGG69YrJVAP7fuT',
                    pk_file='signee1.pk',
                    user=77)

    send = bool(int(sys.argv[1]))
    request_address = 'kQBy01SvmEdBEcL36RABs2bTxto3uykTqlWGnKLn77HIOKRk'
    signee.approve_sign_request(request_address=request_address, 
                                message='~SIGN~',
                                deploy_request_ng=5_000_000,
                                send=send)

    if not send:
        # TODO: address = collection.get_reauest_address_by_signee(...)
        sign = SnftRequest(builder, api, address=request_address)

        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: SIGNATURE REQUEST DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = sign.get_sign_request_data()
        pprint(result)

        print('balance:', sign.balance(True))


if __name__ == '__main__':
    main()
