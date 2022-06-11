from demo.core.contract_base import ContractBase


class NftMarketplace(ContractBase):

    # Configurable properties

    @property
    def owner_address(self): return self._owner_address
    @property
    def market_init_ng(self): return self._market_init_ng

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
        self._owner_address = None
        self._market_init_ng = None


    def deploy(self, script_name='nft-marketplace-deploy', send=True):
        print(f'Deploy NFT marketplace (send={send})')

        params = {
            'owner_address': self.owner_address,
            'market_init_ng': self.market_init_ng,
        }

        result = self.query(params, script_name, send, self.wallet)

        addr_file = result['fif_file'][:-4] + '.addr'
        self.set_address_from_file(addr_file)
        print(f' > contract address: {self.address}')
        print(f'Deploy NFT marketplace (send={send}): DONE')
