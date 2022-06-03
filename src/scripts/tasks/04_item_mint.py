import sys
import yaml
import time
from pprint import pprint

from core.builder import Builder
from core.api_provider_factory import ApiProviderFactory
from contracts.snft_collection import SnftCollection
from contracts.snft_item import SnftItem
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

    item_index = int(sys.argv[1])

    with open('configs/item.yaml') as f:
        config = yaml.safe_load(f)['mint']
        config_item = list(filter(lambda c: c['item_index'] == item_index, config['list']))[0]
        config = {**config, **config_item}

    collection = SnftCollection(builder, api, address='EQCrP6HGSpC4wZyCa-kx6BWKNcfc9pt7mD-xG-cyL3dC6cV9')
    item = SnftItem(builder, api, collection, wallet, user=2)
    item.from_config(config)

    send = bool(int(sys.argv[2]))
    item.mint(send=send)

    if not send:
        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ITEM DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = item.get_nft_data()
        pprint(result)
        
        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: SIGNATURES DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = item.get_signatures_data()
        pprint(result)


if __name__ == '__main__':
    main()
