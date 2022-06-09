
import sys
from pprint import pprint

from core.nft_auction import NftAuction
from core.wallet import Wallet
from tasks.consts import builder, api, wallet, DEFAULT_WALLET_ADDR, DEFAULT_WALLET_PK


AUCTION_ADDRESS = 'EQCMRFoiKQNycZk-oNtCTwsH-KzW0BXd4cRPhCD7Vxl8e4E-'
BIDDER_ADDRESS = 'EQBFC3N-lJCkoxdKTzL6SsIzDMz8_A5x1zo3hgLbraTTN0hB'
BIDDER_WALLET_PK = DEFAULT_WALLET_PK
BID_AMOUNT = 591_000_000


def main():
    # 0. args
    send = bool(int(sys.argv[1]))

    bidder = Wallet(builder, api, address=BIDDER_ADDRESS, pk_file=BIDDER_WALLET_PK)
    bidder.transfer_money(to=AUCTION_ADDRESS, 
                          amount=BID_AMOUNT,
                          send=send)

    # 2. get info
    if not send:
        auction = NftAuction(builder, api, wallet, address=AUCTION_ADDRESS)

        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: AUCTION DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = auction.get_auction_data()
        pprint(result)

        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: GENERAL DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = auction.get_general_data()
        pprint(result)


if __name__ == '__main__':
    main()
