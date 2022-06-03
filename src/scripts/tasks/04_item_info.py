import sys
import yaml
import time
from pprint import pprint

from core.builder import Builder
from core.api_provider_factory import ApiProviderFactory
from contracts.snft_collection import SnftCollection
from contracts.snft_item import SnftItem


def main():
    with open('configs/app.yaml') as f:
        config = yaml.safe_load(f)

    builder = Builder(**config['core'])
    api = ApiProviderFactory.create(config['api'])

    item = SnftItem(builder, api, collection=None, address='EQAOiZWI0ylAIrYahIblh-g3ph14Qp5Gy0AnjpMS72ewxMqZ')

    print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ITEM DATA >>>>>>>>>>>>>>>>>>>>>>>>')
    result = item.get_nft_data()
    pprint(result)
    
    print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: SIGNATURES DATA >>>>>>>>>>>>>>>>>>>>>>>>')
    result = item.get_signatures_data()
    pprint(result)


if __name__ == '__main__':
    main()
