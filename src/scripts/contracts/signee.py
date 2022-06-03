from contracts.wallet import Wallet


class Signee(Wallet):
    def __init__(self,
                 builder,
                 api,
                 address,
                 pk_file,
                 balance=None,
                 user=0,
                 logger=None,
                 log_path='../../logs'):
        super().__init__(builder=builder, 
                         api=api, 
                         address=address,
                         pk_file=pk_file,
                         balance=balance,
                         user=user,
                         logger=logger,
                         log_path=log_path)

    # Smart contract API

    def approve_sign_request(self, request_address, message, deploy_request_ng, 
                             script_name='signee-approve-request', send=True):
        print(f'API: Signee confirm request: object={request_address} (send={send})')

        params = {
            'request_address': request_address,
            'message': message,
            'deploy_request_ng': deploy_request_ng,
            'pk_file': self.pk_file,
        }

        self.query(params, script_name, send, wallet=self)

        print(f'API: Signee confirm request: object={request_address} (send={send}): DONE')
