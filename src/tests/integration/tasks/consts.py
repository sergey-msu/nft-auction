import yaml

from core.builder import Builder
from core.http_api_provider import HttpApiProvider
from core.wallet import Wallet


DEFAULT_WALLET_ADDR = 'EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs'
DEFAULT_WALLET_PK = 'wallet.pk'


with open('configs/app.yaml') as f:
    config = yaml.safe_load(f)

builder = Builder(**config['core'])
builder.compile_sources(**config['compile'])
builder.build_templates(**config['compile'])

api = HttpApiProvider(**config['api'])

wallet = Wallet(builder, api,
                address=DEFAULT_WALLET_ADDR,
                pk_file=DEFAULT_WALLET_PK)
