import os
import pprint
import time
import crc16

from demo.core.utils import addr_from_file, tob64string


class ContractBase:
    def __init__(self,
                 builder,
                 api,
                 wallet=None,
                 address=None,
                 balance=None,
                 logger=None,
                 log_path='../../logs'):
        self.wallet = wallet
        self.logger = logger  # TODO
        self.builder = builder
        self.api = api
        self._state = None
        self._address = address
        self._balance = balance
        self.config = None

    @property
    def address(self):
        return self._address

    def balance(self, last=False):
        if (self._balance is None) or last:
            self._balance = self.api.run_get_balance(self.address)
        return self._balance


    def state(self, last=False):
        if (self._state is None) or last:
            self._state = self.api.run_get_address(self.address)['state']
        return self._state


    def query(self, params, script_name, send, wallet):
        result = {'send': None}

        boc_b64 = self.create_boc(script_name, params, wallet, result)
        if send:
            print(f'Sending {script_name} boc to blockchain...')
            result['send'] = self.api.send_boc(boc_b64)

        return result


    def create_boc(self, script_name, params, wallet, result):
        print(f'Build {script_name} script...')

        if not os.path.exists(self.builder.out_path):
            os.makedirs(self.builder.out_path)

        ts = int(time.time() * 1000)

        tif_file = os.path.join(self.builder.out_path, script_name + '.tif')
        fif_file = os.path.join(self.builder.out_path, script_name + f'-{ts}.fif')
        boc_file = os.path.join(self.builder.out_path, script_name + f'-{ts}-query.boc')

        # fill template with params
        if wallet is not None:
            params['seqno'] = wallet.seqno()
            params['wallet_address'] = wallet.address
        params['script_name'] = script_name
        params['secret_path'] = self.builder.secret_path
        params['out_path'] = self.builder.out_path
        params['ts'] = f'-{ts}'

        print(f'  > script params:\n{pprint.pformat(params)}')
        print(f'  > fill template for "{script_name}"')

        # pass params to tif template
        self.builder.render_template(tif_file,
                                     params=params,
                                     out_file=fif_file,
                                     decorate_str=True)

        # execute fif to get .boc
        self.builder.execute_fif(fif_file)
        if not os.path.exists(boc_file):
            raise Exception(f'File {boc_file} not found after fift script execution.')

        print(f'  > boc generated: {boc_file}')

        with open(boc_file, 'rb') as f:
            boc_b64 = tob64string(f.read())

        print('Build: DONE')

        result['ts'] = ts
        result['tif_file'] = tif_file
        result['fif_file'] = fif_file
        result['boc_file'] = boc_file
        result['boc_b64']  = boc_b64

        return boc_b64


    def set_address_from_file(self, addr_file):
        address = addr_from_file(addr_file)
        if address['b'] is None:
            raise Exception(f'Can\'t find contract address: {addr_file}')

        self._address = address['b']


    def from_config(self, config):
        self.config = config
        for v in vars(self):
            if v.startswith('_') and v[1:] in config:
                value = config[v[1:]]
                setattr(self, v, value)
        return self


    @staticmethod
    def method_id(method_name):
        return (crc16.crc16xmodem(method_name.encode('ascii')) & 0xffff) | 0x10000
