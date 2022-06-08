import sys
from pprint import pprint

from core.nft_collection import NftCollection
from core.nft_item import NftItem
from tasks.consts import builder, api, wallet



NFT_ITEM_CONFIG = {
  'owner_address': 'EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs',
  'coll_ng': 70_000_000,   # 0.07 TON
  'item_ng': 50_000_000,   # 0.05 TON
  'item_index': 2,
  'item_content_uri': 'item?filename=harold.jpg',
}

COLLECTION_ADDRESS = 'EQBZNx4DKEwQR6NmFjH2_3h3PAM6F5mmRdN2n5GNztDVxQ_r'


def main():
    # 0. args
    send = bool(int(sys.argv[1]))

    # 1. mint
    collection = NftCollection(builder, api, address=COLLECTION_ADDRESS)
    item = NftItem(builder, api, collection, wallet)
    item.from_config(NFT_ITEM_CONFIG)
    item.mint(send=send)

    # 2. get info
    if not send:
        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ITEM DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = item.get_nft_data()
        pprint(result)


if __name__ == '__main__':
    main()
