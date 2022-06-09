
import sys
import time
from pprint import pprint

from core.nft_auction import NftAuction
from tasks.consts import builder, api, wallet, DEFAULT_WALLET_ADDR


MARKETPLACE_ADDRESS = 'EQDY2SwQsRuFa_JJZkVMiUtCXh7Eld35lGNLU8kqjlrhRQAW'
NFT_ADDRESS = 'EQBZK1_z9BwM8IP5tqhEB5vccgAB0o8xQKofN_c5Ct2ODiw9'
ROYALTY_ADDRESS = DEFAULT_WALLET_ADDR

AUCTION_CONFIG = {
  'marketplace_address': MARKETPLACE_ADDRESS,
  'nft_address': NFT_ADDRESS,
  'marketplace_fee_address': MARKETPLACE_ADDRESS,
  'marketplace_fee_numer': 10,
  'marketplace_fee_denom': 100,
  'royalty_address': ROYALTY_ADDRESS,
  'royalty_numer': 5,
  'royalty_denom': 100,
  'auction_finish_time': None,
  'auction_salt': 1233557880, # int(time.time()),
  'sniper_before_time': 5,
  'sniper_after_prolong': 10,
  'min_bid':   100_000_000,
  'max_bid': 5_000_000_000,
  'bid_step':   50_000_000,
  'auction_init_ng': 55_000_000,
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
        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: GENERAL DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = auction.get_general_data()
        pprint(result)

        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: MARKETPLACE FEE DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = auction.get_marketplace_fee_data()
        pprint(result)

        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ROYALTY DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = auction.get_royalty_data()
        pprint(result)

        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: AUCTION DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = auction.get_auction_data()
        pprint(result)


if __name__ == '__main__':
    main()
