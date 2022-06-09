
import sys
from pprint import pprint

from core.nft_auction import NftAuction
from core.nft_item import NftItem
from tasks.consts import builder, api, wallet


NFT_ADDRESS = 'EQBZK1_z9BwM8IP5tqhEB5vccgAB0o8xQKofN_c5Ct2ODiw9'
AUCTION_ADDRESS = 'EQCMRFoiKQNycZk-oNtCTwsH-KzW0BXd4cRPhCD7Vxl8e4E-'


def main():
    # 0. args
    send = bool(int(sys.argv[1]))

    # 1. cancel
    auction = NftAuction(builder, api, wallet, address=AUCTION_ADDRESS)
    auction.finish(finish_ng=60_000_000, send=send)

    # 2. get info
    if not send:
        item = NftItem(builder, api, wallet=wallet, address=NFT_ADDRESS)

        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: GENERAL DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = auction.get_general_data()
        pprint(result)

        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: AUCTION DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = auction.get_auction_data()
        pprint(result)

        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ITEM DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = item.get_nft_data()


if __name__ == '__main__':
    main()
