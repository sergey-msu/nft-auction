import base64

from core.utils import addr_from_b64, tob64string
from core.contract_base import ContractBase


class NftAuction(ContractBase):

    # Configurable properties

    @property
    def marketplace_address(self): return self._marketplace_address
    @property
    def nft_address(self): return self._nft_address
    @property
    def marketplace_fee_address(self): return self._marketplace_fee_address
    @property
    def marketplace_fee_numer(self): return self._marketplace_fee_numer
    @property
    def marketplace_fee_denom(self): return self._marketplace_fee_denom
    @property
    def royalty_address(self): return self._royalty_address
    @property
    def royalty_numer(self): return self._royalty_numer
    @property
    def royalty_denom(self): return self._royalty_denom
    @property
    def auction_finish_time(self): return self._auction_finish_time
    @property
    def auction_salt(self): return self._auction_salt
    @property
    def sniper_before_time(self): return self._sniper_before_time
    @property
    def sniper_after_prolong(self): return self._sniper_after_prolong
    @property
    def min_bid(self): return self._min_bid
    @property
    def max_bid(self): return self._max_bid
    @property
    def max_bid(self): return self._max_bid
    @property
    def bid_step(self): return self._bid_step
    @property
    def auction_init_ng(self): return self._auction_init_ng

    # .ctor

    def __init__(self,
                 builder,
                 api,
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

        self._marketplace_address = None
        self._nft_address = None
        self._marketplace_fee_address = None
        self._marketplace_fee_numer = None
        self._marketplace_fee_denom = None
        self._royalty_address = None
        self._royalty_numer = None
        self._royalty_denom = None
        self._auction_finish_time = None
        self._auction_salt = None
        self._sniper_before_time = None
        self._sniper_after_prolong = None
        self._min_bid = None
        self._max_bid = None
        self._max_bid = None
        self._bid_step = None
        self._auction_init_ng = None

    # Smart Contract deploy to Blockchain

    def deploy(self, script_name='nft-auction-deploy', send=True):
        print(f'Deploy NFT Auction (send={send})')

        params = {
            'marketplace_address': self.marketplace_address,
            'nft_address': self.nft_address,
            'marketplace_fee_address': self.marketplace_fee_address,
            'marketplace_fee_numer': self.marketplace_fee_numer,
            'marketplace_fee_denom': self.marketplace_fee_denom,
            'royalty_address': self.royalty_address,
            'royalty_numer': self.royalty_numer,
            'royalty_denom': self.royalty_denom,
            'auction_finish_time': self.auction_finish_time,
            'auction_salt': self.auction_salt,
            'sniper_before_time': self.sniper_before_time,
            'sniper_after_prolong': self.sniper_after_prolong,
            'min_bid': self.min_bid,
            'max_bid': self.max_bid,
            'bid_step': self.bid_step,
            'auction_init_ng': self.auction_init_ng,
        }

        result = self.query(params, script_name, send, self.wallet)

        addr_file = result['fif_file'][:-4] + '.addr'
        self.set_address_from_file(addr_file)
        print(f' > contract address: {self.address}')
        print(f'Deploy NFT Auction (send={send}): DONE')

    # Smart Contract API

    # TODO

    # Smart Contract GET methods

    def get_general_data(self):
        result = self.api.run_get(self.address, 'get_general_data')
        if result and len(result) == 3:
            return {
                'marketplace_address': addr_from_b64(result[0][1]['object']['data']['b64'])['b'],
                'nft_address': addr_from_b64(result[1][1]['object']['data']['b64'])['b'],
                'nft_owner_address': addr_from_b64(result[2][1]['object']['data']['b64'])['b'],
            }

        return None


    def get_marketplace_fee_data(self):
        result = self.api.run_get(self.address, 'get_marketplace_fee_data')

        if result and len(result) == 3:
            return {
                'marketplace_fee_address': addr_from_b64(result[0][1]['object']['data']['b64'])['b'],
                'marketplace_fee_numer': int(result[1][1], 16),
                'marketplace_fee_denom': int(result[2][1], 16),
            }

        return None


    def get_royalty_data(self):
        result = self.api.run_get(self.address, 'get_royalty_data')

        if result and len(result) == 3:
            return {
                'royalty_address': addr_from_b64(result[0][1]['object']['data']['b64'])['b'],
                'royalty_numer': int(result[1][1], 16),
                'royalty_denom': int(result[2][1], 16),
            }

        return None


    def get_auction_data(self):
        result = self.api.run_get(self.address, 'get_auction_data')

        if result and len(result) == 11:
            return {
                'auction_finish_time': int(result[0][1], 16) if result[0][1] else None,
                'auction_salt': int(result[1][1], 16),
                'sniper_before_time': int(result[2][1], 16),
                'sniper_after_prolong': int(result[3][1], 16),
                'min_bid_value': int(result[4][1], 16),
                'max_bid_value': int(result[5][1], 16) if result[0][1] else None,
                'bid_step_value': int(result[6][1], 16),
                'curr_winner_address': addr_from_b64(result[7][1]['object']['data']['b64'])['b'],
                'curr_winner_bid': int(result[6][1], 16),
                'is_finished': int(result[6][1], 16) == -1,
                'is_cancelled': int(result[6][1], 16) == -1,
            }

        return None
