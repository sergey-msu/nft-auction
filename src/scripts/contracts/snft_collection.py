import base64

from utils import addr_from_b64, tob64string
from contracts.contract_signable import Signable


class SnftCollection(Signable):

    # Configurable properties

    @property
    def collection_content_uri(self): return self._collection_content_uri
    @property
    def item_content_base_uri(self): return self._item_content_base_uri
    @property
    def royalty_base(self): return self._royalty_base
    @property
    def royalty_factor(self): return self._royalty_factor
    @property
    def coll_init_ng(self): return self._coll_init_ng
    @property
    def owner_address(self): return self._owner_address
    @property
    def royalty_address(self): return self._royalty_address

    # .ctor

    def __init__(self,
                 builder,
                 api,
                 wallet=None,
                 user=None,
                 address=None,
                 balance=None,
                 logger=None,
                 log_path='../../logs'):
        super().__init__(builder=builder, 
                         api=api, 
                         wallet=wallet,
                         address=address,
                         balance=balance,
                         user=user,
                         logger=logger,
                         log_path=log_path)

        self._collection_content_uri = None
        self._item_content_base_uri = None
        self._royalty_base = None
        self._royalty_factor = None
        self._coll_init_ng = None
        self._owner_address = None
        self._royalty_address = None

    # Smart Contract deploy to Blockchain
    
    def deploy(self, script_name='snft-collection-deploy', send=True):
        print(f'Deploy SNFT Collection (send={send})')

        params = {
            'sign_max_number': self.sign_max_number,
            'sign_deploy_fee': self.sign_deploy_fee,
            'sign_commit_fee': self.sign_commit_fee,
            'min_stake': self.min_stake,
            'collection_content_uri': tob64string(self.collection_content_uri.encode('utf-8')),
            'item_content_base_uri': tob64string(self.item_content_base_uri.encode('utf-8')),
            'royalty_base': self.royalty_base,
            'royalty_factor': self.royalty_factor,
            'coll_init_ng': self.coll_init_ng,
            'owner_address': self.owner_address,
            'royalty_address': self.royalty_address,
            'provider_address': self.provider_address,
        }

        result = self.query(params, script_name, send, self.wallet)

        addr_file = result['fif_file'][:-4] + '.addr'
        self.set_address_from_file(addr_file)
        print(f' > contract address: {self.address}')
        print(f'Deploy SNFT Collection (send={send}): DONE')

    # Smart Contract API

    # TODO

    # Smart Contract GET methods

    def get_collection_data(self):
        result = self.api.run_get(self.address, 'get_collection_data')

        if result and len(result) == 3:
            return {
                'next_item_index': int(result[0][1], 16),
                'collection_data': base64.b64decode(result[1][1]['object']['data']['b64'])[1:].decode('utf-8'),
                'owner_address': addr_from_b64(result[2][1]['object']['data']['b64'])['b'],
            }

        return None


    def royalty_params(self):
        result = self.api.run_get(self.address, 'royalty_params')

        if result and len(result) == 3:
            return {
                'royalty_factor': int(result[0][1], 16),
                'royalty_base': int(result[1][1], 16),
                'royalty_address': addr_from_b64(result[2][1]['object']['data']['b64'])['b'],
            }

        return None


    def get_nft_address_by_index(self, index):
        result = self.api.run_get(self.address, 
                                  'get_nft_address_by_index',
                                  stack=[['num', index]])

        if result and len(result) == 1:
            return {
                'nft_address': addr_from_b64(result[0][1]['object']['data']['b64'])['b'],
            }

        return None


    def get_nft_content(self, index):
        # TODO: tvm.Cell = nftData.contentCell.toBoc
        # A BUG, not ready yet: https://t.me/tondev/66903
        result = self.provider.run_get(self.address,
                                       'get_nft_content',
                                       stack=[['num', index], ['tvm.Cell', None]])

        if result and len(result) == 1:
            return {
                'collection_data': base64.b64decode(result[1][1]['object']['data']['b64'])[1:].decode('utf-8'),
                'nft_address': addr_from_b64(result[0][1]['object']['data']['b64'])['b'],
            }

        return None
