import base64

from demo.core.utils import addr_from_b64
from demo.core.contract_base import ContractBase


class NftItem(ContractBase):

    # Configurable properties

    @property
    def owner_address(self): return self._owner_address
    @property
    def coll_ng(self): return self._coll_ng
    @property
    def item_ng(self): return self._item_ng
    @property
    def item_index(self): return self._item_index
    @property
    def item_content_uri(self): return self._item_content_uri

    # .ctor

    def __init__(self,
                 builder,
                 api,
                 collection=None,
                 wallet=None,
                 address=None,
                 balance=None,
                 logger=None,
                 log_path='../../logs'):
        super().__init__(builder=builder, 
                         api=api, 
                         wallet=wallet,
                         address=address,
                         balance=balance,
                         logger=logger,
                         log_path=log_path)

        self.collection = collection

        self._owner_address = None
        self._coll_ng = None
        self._item_ng = None
        self._item_index = None
        self._item_content_uri = None


    @property
    def address(self):
        if self._address is not None:
            return self._address

        self._address = self.collection.get_nft_address_by_index(self.item_index)['nft_address']

        return self._address


    # Smart Contract deploy to Blockchain

    def mint(self, script_name='nft-item-mint', send=True):
        print(f'Mint NFT Item (send={send})')

        params = {
            'item_index': self.item_index,
            'item_content_uri': base64.b64encode(self.item_content_uri.encode('utf-8')).decode('utf-8'),
            'coll_ng': self.coll_ng,
            'item_ng': self.item_ng,
            'owner_address': self.owner_address,
            'coll_address': self.collection.address,
        }

        self.query(params, script_name, send, self.wallet)

        print(f' > contract address: {self.address}')
        print(f'Mint NFT Item (send={send}): DONE')


    # Smart contract API

    def transfer_ownership(self, 
                           new_owner_address, 
                           item_ng=100_000_000, 
                           forward_amount=None, 
                           script_name='nft-item-transfer', send=True):
        print(f'API: NFT Item transfer ownership to {new_owner_address} (send={send})')

        params = {
            'new_owner_address': new_owner_address,
            'item_ng': item_ng,
            'forward_amount': forward_amount or item_ng,
            'item_address': self.address,
        }

        self.query(params, script_name, send, self.wallet)

        print(f'API: NFT Item transfer ownership to {new_owner_address} (send={send}): DONE')


    # Smart Contract GET methods

    def get_nft_data(self):
        result = self.api.run_get(self.address, 'get_nft_data')
        if not result['ok']:
            raise Exception(result['message'])

        if result and len(result) == 5:
            return {
                'is_init': int(result[0][1], 16) == -1,
                'index': int(result[1][1], 16),
                'collection_address': addr_from_b64(result[2][1]['object']['data']['b64'])['b'],
                'owner_address': addr_from_b64(result[3][1]['object']['data']['b64'])['b'],
                'content': base64.b64decode(result[4][1]['object']['data']['b64']).decode('utf-8'),
            }

        return None
