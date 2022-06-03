import time

from contracts.contract_base import ContractBase


class Wallet(ContractBase):
    def __init__(self,
                 builder,
                 api,
                 address=None,
                 pk_file='wallet.pk',
                 balance=None,
                 user=0,
                 wait_sec=1,
                 wait_max_iters=20,
                 logger=None,
                 log_path='../../logs'):
        super().__init__(builder=builder, 
                         api=api, 
                         address=address,
                         balance=balance,
                         user=user,
                         logger=logger,
                         log_path=log_path)

        self.wait_sec = wait_sec
        self.wait_max_iters = wait_max_iters
        self.pk_file = pk_file
        self._seqno = None


    def deploy(self, seed_id, generate_private_key, wc,
               script_name='new-simple-wallet', send=True):
        print(f'Deploy simple wallet (send={send})')

        params = {
            'seed_id': seed_id,
            'generate_private_key': generate_private_key,
            'pk_file': self.pk_file,
            'wc': wc,
        }

        result = self.query(params, script_name, send, wallet=None)

        addr_file = result['fif_file'][:-4] + '.addr'
        self.set_address_from_file(addr_file)
        print(f' > contract address: {self.address}')
        print(f'Deploy simple wallet (send={send}): DONE')


    def seqno(self, wait=False):
        if self._seqno is None:
            result = self.api.run_get(self.address, 'seqno')
            self._seqno = int(result[0][1], 16)
            return self._seqno

        if wait:
            prev_seqno = self._seqno
            iter = 0

            while True:
                time.sleep(self.wait_sec)
                iter += 1
                result = self.api.run_get(self.address, 'seqno')
                curr_seqno = int(result[0][1], 16)

                if (prev_seqno < curr_seqno) or \
                   (iter > self.wait_max_iters):
                    break

            self._seqno = curr_seqno

        return self._seqno


    def transfer_money(self, to, amount, 
                       script_name='wallet-transfer-money', send=True):
        print(f'API: Transfer {amount} coins from {self.address} to {to} (send={send})')

        params = {
            'to_address': to,
            'amount': amount,
            'wallet_pk_file': self.pk_file,
        }
        self.query(params, script_name, send, self)

        print(f'API: Transfer money (send={send}): DONE')
