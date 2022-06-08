
import sys
from pprint import pprint

from core.nft_auction import NftAuction
from core.nft_item import NftItem
from tasks.consts import builder, api, wallet, DEFAULT_WALLET_ADDR


NFT_ADDRESS = 'EQCXM6ixoJrUhxY8JSBJGm7o8_Akvpa5mwPZ0nMEj9VQvAKz'
AUCTION_ADDRESS = 'EQANPb2vh5Q-iJTm-0azR4kVL2Viy4_5kJTRBAZVVV6grwdX'


def main():
    # 0. args
    send = bool(int(sys.argv[1]))

    # 1. deploy
    item = NftItem(builder, api, wallet=wallet, address=NFT_ADDRESS)
    item.transfer_ownership(new_owner_address=AUCTION_ADDRESS, 
                            forward_amount=100_000_000,
                            item_ng=200_000_000, send=send)

    # 2. get info
    if not send:
        auction = NftAuction(builder, api, wallet, address=AUCTION_ADDRESS)

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
