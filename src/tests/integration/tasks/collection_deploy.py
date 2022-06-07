
import sys
from pprint import pprint

from core.nft_collection import NftCollection
from tasks.consts import builder, api, wallet


COLLECTION_CONFIG = {
  'collection_content_uri': 'https://myorg.com/collection1.json',
  'item_content_base_uri':  'https://myorg.com/',
  'royalty_base':   100,
  'royalty_factor': 5,             # 5% royalty
  'coll_init_ng':   50_000_000,    # 0.05 TON
  'owner_address':    'EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs',
  'royalty_address':  'EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs',
}


def main():
    # 0. args
    send = bool(int(sys.argv[1]))

    # 1. deploy
    collection = NftCollection(builder, api, wallet)
    collection.from_config(COLLECTION_CONFIG)
    collection.deploy(send=send)

    # 2. get info
    if not send:
        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: COLLECTION DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = collection.get_collection_data()
        pprint(result)

        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ROYALTY DATA >>>>>>>>>>>>>>>>>>>>>>>>')
        result = collection.royalty_params()
        pprint(result)
        
        print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ITEM ADDR BY INDEX >>>>>>>>>>>>>>>>>>>>>>>>')
        result = collection.get_nft_address_by_index(0)
        pprint(result)


if __name__ == '__main__':
    main()
