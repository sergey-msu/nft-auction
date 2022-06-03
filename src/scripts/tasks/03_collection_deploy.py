import sys
import yaml
from pprint import pprint

from core.builder import Builder
from core.api_provider_factory import ApiProviderFactory
from contracts.snft_collection import SnftCollection
from contracts.wallet import Wallet


def main():
    with open('configs/app.yaml') as f:
        config = yaml.safe_load(f)

    builder = Builder(**config['core'])
    api = ApiProviderFactory.create(config['api'])

    builder.clear_out()
    builder.compile_sources(**config['compile'])
    builder.build_templates(**config['compile'])

    wallet = Wallet(builder, api,
                    address=config['core']['wallet_address'],
                    pk_file=config['core']['wallet_pk'],
                    user=1)

    with open('configs/collection.yaml') as f:
        config = yaml.safe_load(f)['deploy']

    collection = SnftCollection(builder, api, wallet, user=1)
    collection.from_config(config)

    send = bool(int(sys.argv[1]))
    collection.deploy(send=send)

    if not send:
        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: COLLECTION DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = collection.get_collection_data()
        pprint(result)

        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ROYALTY DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = collection.royalty_params()
        pprint(result)
        
        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ITEM ADDR BY INDEX >>>>>>>>>>>>>>>>>>>>>>>>')
        result = collection.get_nft_address_by_index(0)
        pprint(result)
        
        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: SIGNATURES DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = collection.get_signatures_data()
        pprint(result)


if __name__ == '__main__':
    main()
