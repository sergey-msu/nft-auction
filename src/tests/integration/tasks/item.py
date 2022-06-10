import yaml
from pprint import pprint

from tests.integration.core.builder import Builder
from tests.integration.core.http_api_provider import HttpApiProvider
from tests.integration.core.wallet import Wallet
from tests.integration.core.nft_collection import NftCollection
from tests.integration.core.nft_item import NftItem


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


def mint(coll_addr, index, wallet_addr, owner_addr, coll_ng=70_000_000, init_ng=50_000_000, send=True, private_key='wallet.pk', **kwargs):
    print('Mininting NFT item...')

    wallet = Wallet(builder, api, address=wallet_addr, pk_file=private_key)
    collection = NftCollection(builder, api, wallet, address=coll_addr)
    config = {
        'owner_address': owner_addr,
        'item_index': index,
        'coll_ng': coll_ng,
        'item_ng': init_ng,
        'item_content_uri': 'item?filename=harold.jpg',
    }
    item = NftItem(builder, api, collection, wallet)
    item.from_config(config)
    item.mint(send=send)

    print(f'\nNFT item address: {item.address}\n')


def transfer(addr, wallet_addr, to_addr, item_ng=80_000_000, forw_ng=50_000_000, send=True, private_key='wallet.pk', **kwargs):
    print(f'Transferring NFT item to {to_addr}...')

    wallet = Wallet(builder, api, address=wallet_addr, pk_file=private_key)
    item = NftItem(builder, api, wallet=wallet, address=addr)

    item.transfer_ownership(new_owner_address=to_addr, 
                            forward_amount=forw_ng,
                            item_ng=item_ng, send=send)


def info(addr, **kwargs):
    item = NftItem(builder, api, address=addr)

    print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ITEM DATA >>>>>>>>>>>>>>>>>>>>>>>>')
    result = item.get_nft_data()
    pprint(result)


def run_item(command, **kwargs):
    init()

    if command == 'mint':
        mint(**kwargs)
    elif command == 'info':
        info(**kwargs)
    elif command == 'transfer':
        transfer(**kwargs)
    else:
      raise Exception(f'Unknown command {command}')
