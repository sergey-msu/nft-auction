import sys
import yaml
import time
from pprint import pprint

from core.builder import Builder
from core.api_provider_factory import ApiProviderFactory
from contracts.snft_collection import SnftCollection
from contracts.snft_item import SnftItem
from contracts.wallet import Wallet


def main():
    with open('configs/app.yaml') as f:
        config = yaml.safe_load(f)

    builder = Builder(**config['core'])
    api = ApiProviderFactory.create(config['api'])

    builder.clear_out()
    builder.compile_sources(**config['compile'])
    builder.build_templates(**config['compile'])

    owner_wallet = Wallet(builder, api, address='EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs', pk_file='wallet.pk')

    collection = SnftCollection(builder, api, address='EQCm83drJjxoYdBLsbGyz6X-fAwixIahbgjNB_qJttvtlwgG')
    item = SnftItem(builder, api, collection, wallet=owner_wallet,
                    address='EQC-5uvYa0iPoabaX5S_V4UxLmajNPYLZ0qkH9J0DXyLIoyG', user=3)

    send = bool(int(sys.argv[1]))
    item.transfer_ownership(new_owner_address='EQALMaIEwGADZD-K13tjJK_JUcCshWVFxtgFEiNGXKXYV_Bv', 
                            item_ng=100_000_000, send=send)

    if send:
        time.sleep(20)

    print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ITEM DATA >>>>>>>>>>>>>>>>>>>>>>>>')
    result = item.get_nft_data()
    pprint(result)

    print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: SIGNATURES DATA >>>>>>>>>>>>>>>>>>>>>>>>')
    result = item.get_signatures_data()
    pprint(result)


if __name__ == '__main__':
    main()
