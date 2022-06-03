from os import O_NONBLOCK
from contracts.wallet import Wallet


class SnftProvider(Wallet):
    def __init__(self,
                 builder,
                 api,
                 address=None,
                 pk_file='provider.pk',
                 balance=None,
                 user=0,
                 wait_sec=1,
                 wait_max_iters=20,
                 logger=None,
                 log_path='../../logs'):
        super().__init__(builder=builder, 
                         api=api, 
                         address=address,
                         pk_file=pk_file,
                         balance=balance,
                         user=user,
                         wait_sec=wait_sec,
                         wait_max_iters=wait_max_iters,
                         logger=logger,
                         log_path=log_path)

    # Deploy new Provider to Blockchain

    def deploy(self, seed_id, generate_private_key, wc,
               script_name='new-provider', send=True):
        super().deploy(seed_id, generate_private_key, wc, script_name, send)

    # Smart contract API

    def open_sign_request(self,
                          object_address,
                          signee_address,
                          network_id, 
                          network_address, 
                          deploy_request_ng, 
                          open_request_ng,
                          content_uri,
                          script_name='snft-provider-open-request', send=True):
        print(f'API: SNFT provider open signature request: object={object_address} signee={signee_address} (send={send})')

        params = {
            'provider_address': self.address,
            'signee_address': signee_address,
            'object_address': object_address,
            'network_id': network_id,
            'network_address': network_address,
            'deploy_request_ng': deploy_request_ng,
            'open_request_ng': open_request_ng,
            'content_uri': content_uri,
        }

        self.query(params, script_name, send, wallet=self)

        print(f'API: SNFT provider open signature request: object={object_address} signee={signee_address} (send={send}): DONE')

    def cancel_sign_request(self,
                            object_address,
                            signee_address,
                            deploy_request_ng,
                            script_name='snft-provider-cancel-request', send=True):
        print(f'API: SNFT provider cancel signature request: object={object_address} signee={signee_address} (send={send})')

        params = {
            'provider_address': self.address,
            'signee_address': signee_address,
            'object_address': object_address,
            'deploy_request_ng': deploy_request_ng,
        }

        self.query(params, script_name, send, wallet=self)

        print(f'API: SNFT provider cancel signature request: object={object_address} signee={signee_address} (send={send}): DONE')
