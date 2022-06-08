
import sys
from pprint import pprint

from core.nft_auction import NftAuction
from tasks.consts import builder, api, wallet


AUCTION_ADDRESS = 'EQDxGpmsvfBz4-gcZzZnP_Iv_-bcE2C6W1JluxBsCBqVtNDT'


def main():
    # 0. args
    send = bool(int(sys.argv[1]))

    # 1. cancel
    auction = NftAuction(builder, api, wallet, address=AUCTION_ADDRESS)
    auction.cancel(cancel_ng=100_000_000, send=send)

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
