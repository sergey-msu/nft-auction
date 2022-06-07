
import sys
from pprint import pprint

from core.nft_marketplace import NftMarketplace
from tasks.consts import builder, api, wallet


MARKETPLACE_CONFIG = {
  'owner_address': 'EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs',
  'market_init_ng': 50_000_000,    # 0.05 TON
}


def main():
    # 0. args
    send = bool(int(sys.argv[1]))

    # 1. deploy
    marketplace = NftMarketplace(builder, api, wallet)
    marketplace.from_config(MARKETPLACE_CONFIG)
    marketplace.deploy(send=send)


if __name__ == '__main__':
    main()
