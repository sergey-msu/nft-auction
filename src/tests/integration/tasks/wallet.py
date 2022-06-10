import yaml

from tests.integration.core.builder import Builder
from tests.integration.core.http_api_provider import HttpApiProvider
from tests.integration.core.wallet import Wallet


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



def seqno(private_key='wallet.pk', **kwargs):
  wallet = Wallet(builder, api, pk_file=private_key)
  print('seqno:', wallet.seqno())


def deploy(seed, send=True, generate_key=0, private_key='wallet.pk', **kwargs):
    print('Deploying wallet...')

    wallet = Wallet(builder, api, pk_file=private_key)
    wallet.deploy(seed, generate_private_key=generate_key, wc="0", send=send)

    print(f'\nWallet address: {wallet.address}\n')


def transfer(from_addr, to_addr, amount, private_key='wallet.pk', **kwargs):
  wallet = Wallet(builder, api, address=from_addr, pk_file=private_key)
  wallet.transfer_money(to=to_addr, amount=amount, send=True)


def run_wallet(command, **kwargs):
    init()

    if command == 'new':
        deploy(**kwargs)
    elif command == 'seqno':
        seqno(**kwargs)
    elif command == 'transfer':
        transfer(**kwargs)
    else:
      raise Exception(f'Unknown command {command}')
