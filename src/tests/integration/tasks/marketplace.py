import yaml

from tests.integration.core.builder import Builder
from tests.integration.core.http_api_provider import HttpApiProvider
from tests.integration.core.wallet import Wallet
from tests.integration.core.nft_marketplace import NftMarketplace


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


def deploy(wallet_addr, owner_addr, init_ng, send=True, private_key='wallet.pk', **kwargs):
    print('Deploying marketplace...')

    wallet = Wallet(builder, api, address=wallet_addr, pk_file=private_key)
    marketplace = NftMarketplace(builder, api, wallet)
    config = {
      'owner_address': owner_addr,
      'market_init_ng': init_ng,
    }
    marketplace.from_config(config)
    marketplace.deploy(send=send)

    print(f'\nMarketplace address: {marketplace.address}\n')


def run_marketplace(command, **kwargs):
    init()

    if command == 'new':
        deploy(**kwargs)
    else:
      raise Exception(f'Unknown command {command}')
