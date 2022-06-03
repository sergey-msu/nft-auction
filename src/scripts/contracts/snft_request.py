import base64

from contracts.contract_base import ContractBase
from utils import addr_from_b64


class SnftRequest(ContractBase):
    def __init__(self,
                 builder,
                 api,
                 address,
                 balance=None,
                 user=0,
                 logger=None,
                 log_path='../../logs'):
        super().__init__(builder=builder, 
                         api=api, 
                         address=address,
                         balance=balance,
                         user=user,
                         logger=logger,
                         log_path=log_path)


    # Smart Contract GET methonds

    def get_sign_request_data(self):
        result = self.api.run_get(self.address, 'get_sign_request_data')

        if result and len(result) == 11:
            return {
                'is_init': int(result[0][1], 16) == -1,
                'object_address': addr_from_b64(result[1][1]['object']['data']['b64'])['b'],
                'signee_address': addr_from_b64(result[2][1]['object']['data']['b64'])['b'],
                'provider_address': addr_from_b64(result[3][1]['object']['data']['b64'])['b'],
                'sign_commit_fee': int(result[4][1], 16),
                'min_stake': int(result[5][1], 16),
                'network_id': int(result[6][1], 16),
                'network_address': int(result[7][1], 16),
                'is_approved': int(result[8][1], 16) == -1,
                'content': base64.b64decode(result[9][1]['object']['data']['b64']).decode('utf-8')[1:],
                'message': base64.b64decode(result[10][1]['object']['data']['b64']).decode('utf-8'),
            }

        return None
