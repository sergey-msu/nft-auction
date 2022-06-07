import sys
from pprint import pprint

from core.nft_collection import NftCollection
from core.nft_item import NftItem
from tasks.consts import builder, api, wallet


def main():
    # 0. args
    send = bool(int(sys.argv[1]))

    # 1. transfer
    owner_wallet = wallet  # may change
    collection = NftCollection(builder, api, address='EQBZNx4DKEwQR6NmFjH2_3h3PAM6F5mmRdN2n5GNztDVxQ_r')
    item = NftItem(builder, api, collection, wallet=owner_wallet,
                   address='EQDCb78JFeofTGoUuiWxJbscquqNdCnjFQav2M7XBXKQ1MfS')

    item.transfer_ownership(new_owner_address='EQBFC3N-lJCkoxdKTzL6SsIzDMz8_A5x1zo3hgLbraTTN0hB', 
                            item_ng=100_000_000, send=send)

    if not send:
        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ITEM DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = item.get_nft_data()
        pprint(result)


if __name__ == '__main__':
    main()
