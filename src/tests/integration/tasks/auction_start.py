
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

    # 1. start auction by simple transfer transaction from NFT
    item = NftItem(builder, api, wallet=wallet, address=NFT_ADDRESS)
    item.transfer_ownership(new_owner_address=AUCTION_ADDRESS, 
                            forward_amount=100_000_000,
                            item_ng=200_000_000, send=send)

    # 2. get info
    if not send:
        auction = NftAuction(builder, api, wallet, address=AUCTION_ADDRESS)

        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: MARKETPLACE FEE DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = auction.get_marketplace_fee_data()
        pprint(result)

        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: GENERAL DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = auction.get_general_data()
        pprint(result)

        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ITEM DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = item.get_nft_data()
        pprint(result)


if __name__ == '__main__':
    main()
