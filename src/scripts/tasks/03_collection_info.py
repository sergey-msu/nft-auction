import yaml
import time
from pprint import pprint

from core.builder import Builder
from core.api_provider_factory import ApiProviderFactory
from contracts.snft_collection import SnftCollection


def main():
    with open('configs/app.yaml') as f:
        config = yaml.safe_load(f)

    builder = Builder(**config['core'])
    api = ApiProviderFactory.create(config['api'])

    collection = SnftCollection(builder, api, address='EQAQRTYzzAz3DMhMLhLLwScDO-nXJoJHY6zlBUz04QE3qIev')
    
    print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: COLLECTION DATA >>>>>>>>>>>>>>>>>>>>>>>>')
    result = collection.get_collection_data()
    pprint(result)

    # wait in mainnet (too many requests)
    # time.sleep(3)
    
    print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ROYALTY DATA >>>>>>>>>>>>>>>>>>>>>>>>')
    result = collection.royalty_params()
    pprint(result)
    
    print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ITEM ADDR BY INDEX >>>>>>>>>>>>>>>>>>>>>>>>')
    result = collection.get_nft_address_by_index(0)
    pprint(result)
    
    print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: SIGNATURES DATA >>>>>>>>>>>>>>>>>>>>>>>>')
    result = collection.get_signatures_data()
    pprint(result)


if __name__ == '__main__':
    main()
