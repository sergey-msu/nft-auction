
import sys
from pprint import pprint

from core.nft_auction import NftAuction
from tasks.consts import builder, api, wallet


AUCTION_CONFIG = {
  'owner_address': 'EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs',
  'market_init_ng': 50_000_000,    # 0.05 TON
}


def main():
    # 0. args
    send = bool(int(sys.argv[1]))

    # 1. deploy
    auction = NftAuction(builder, api, wallet)
    auction.from_config(AUCTION_CONFIG)
    auction.deploy(send=send)

    # 2. get info
    if not send:
        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: AUCTION DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = auction.get_auction_data()
        pprint(result)

        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ROYALTY DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = collection.royalty_params()
        pprint(result)
        
        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ITEM ADDR BY INDEX >>>>>>>>>>>>>>>>>>>>>>>>')
        result = collection.get_nft_address_by_index(0)
        pprint(result)


if __name__ == '__main__':
    main()
