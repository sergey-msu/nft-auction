import yaml

from demo.core.builder import Builder
from demo.core.http_api_provider import HttpApiProvider


# constants

SANDBOX = 'https://sandbox.tonwhales.com/explorer/address/{addr}'

MARKETPLACE = 'EQDY2SwQsRuFa_JJZkVMiUtCXh7Eld35lGNLU8kqjlrhRQAW'
WALLET1 = 'EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs'
WALLET2 = 'EQBFC3N-lJCkoxdKTzL6SsIzDMz8_A5x1zo3hgLbraTTN0hB'
WALLET3 = 'EQDj86RXZrSzO-MN5gjgRjuMDucqATYq2kcamMQZZhAbY4j0'
PRIVATE_KEY = 'wallet.pk'
INIT_NG = 50000000
COLL_NG = 70000000
COLL_OWNER_ADDR = WALLET1
ROYALTY_ADDR = WALLET1

# API

with open('demo/configs/app.yaml') as f:
  config = yaml.safe_load(f)

BUILDER = Builder(**config['core'])
BUILDER.compile_sources(**config['compile'])
BUILDER.build_templates(**config['compile'])
API = HttpApiProvider(**config['api'])


def trim_center(s, f=7, t=7):
    return s[:f] + '...' + s[-t:]
