import base64

from utils import addr_from_b64, addr_from_b64_cell, tob64string
from contracts.contract_base import ContractBase


class Signable(ContractBase):

    # Configurable properties

    @property
    def sign_max_number(self): return self._sign_max_number
    @property
    def sign_deploy_fee(self): return self._sign_deploy_fee
    @property
    def sign_commit_fee(self): return self._sign_commit_fee
    @property
    def min_stake(self): return self._min_stake
    @property
    def provider_address(self): return self._provider_address

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
                         address=address,
                         balance=balance,
                         user=user,
                         logger=logger,
                         log_path=log_path)

        self.wallet = wallet

        self._sign_max_number = None
        self._sign_deploy_fee = None
        self._sign_commit_fee = None
        self._min_stake = None
        self._provider_address = None

    # Smart Contract GET methods

    def get_signatures_data(self):
        result = self.api.run_get(self.address, 'get_signatures_data')

        if result and len(result) == 7:
            sign_max_number = int(result[0][1], 16)
            sign_number = int(result[1][1], 16)
            sign_deploy_fee = int(result[2][1], 16)
            sign_commit_fee = int(result[3][1], 16)
            min_stake = int(result[4][1], 16)

            sign_provider_address = addr_from_b64(result[5][1]['object']['data']['b64'])['b']

            # signatures
            signatures = []
            for p in result[6][1]['elements']:
                signature = addr_from_b64_cell(p['cell']['bytes'])['b']
                signatures.append(signature)

        return {
                'sign_max_number': sign_max_number,
                'sign_number': sign_number,
                'sign_deploy_fee': sign_deploy_fee,
                'sign_commit_fee': sign_commit_fee,
                'min_stake': min_stake,
                'sign_provider_address': sign_provider_address,
                'signatures': signatures,
            }

        return None
