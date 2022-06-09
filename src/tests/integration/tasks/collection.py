from typing import Collection
import yaml
from pprint import pprint

from tests.integration.core.builder import Builder
from tests.integration.core.http_api_provider import HttpApiProvider
from tests.integration.core.wallet import Wallet
from tests.integration.core.nft_collection import NftCollection


builder = None
api = None


def init():
  with open('tests/integration/configs/app.yaml') as f:
      config = yaml.safe_load(f)

  global builder
  builder = Builder(**config['core'])
  builder.compile_sources(**config['compile'])
  builder.build_templates(**config['compile'])

  global api
  api = HttpApiProvider(**config['api'])


def deploy(seed, wallet_addr, owner_addr, royalty_address, init_ng=50_000_000, send=True, private_key='wallet.pk', **kwargs):
    print('Deploying collection...')

    wallet = Wallet(builder, api, address=wallet_addr, pk_file=private_key)
    collection = NftCollection(builder, api, wallet)
    config = {
      'collection_content_uri': f'https://myorg.com/collection{seed}.json',
      'item_content_base_uri':  'https://myorg.com/',
      'royalty_base':   100,
      'royalty_factor': 5,             # 5% royalty
      'coll_init_ng':   init_ng,
      'owner_address':    owner_addr,
      'royalty_address':  royalty_address,
    }
    collection.from_config(config)
    collection.deploy(send=send)

    print(f'\nCollection address: {collection.address}\n')


def info(addr, **kwargs):
    collection = NftCollection(builder, api, address=addr)

    print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: COLLECTION DATA >>>>>>>>>>>>>>>>>>>>>>>>')
    result = collection.get_collection_data()
    pprint(result)

    print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ROYALTY DATA >>>>>>>>>>>>>>>>>>>>>>>>')
    result = collection.royalty_params()
    pprint(result)
    
    print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ITEM ADDR BY INDEX >>>>>>>>>>>>>>>>>>>>>>>>')
    result = collection.get_nft_address_by_index(0)
    pprint(result)


def run_collection(command, **kwargs):
    init()

    if command == 'deploy':
        deploy(**kwargs)
    elif command == 'info':
        info(**kwargs)
    else:
      raise Exception(f'Unknown command {command}')
