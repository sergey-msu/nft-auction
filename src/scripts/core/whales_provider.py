import json
import requests
import base64


class WhalesApiProvider:
    def __init__(self, api_base_url, api_key, wait_sec, wait_max_iters):
        self.api_base_url = api_base_url
        self.api_key = api_key
        self.wait_sec = wait_sec
        self.wait_max_iters = wait_max_iters
        self.current_seqnos = {}


    def send_boc(self, boc_b64):
        data = {'boc': boc_b64}
        return self._post('sendBoc', data=data)


    def send_boc_file(self, boc_file):
        with open(boc_file, 'rb') as f:
            boc_b64 = base64.b64encode(f.read()).decode('utf8')

        return self.send_boc(boc_b64)


    def run_get(self, smc_addr, smc_method, stack=None):
        result = self._post('runGetMethod', smc_addr=smc_addr, smc_method=smc_method, stack=stack)
        return result['stack']

    def run_get_balance(self, address):
        url = f'{self.api_base_url}getAddressBalance?api_key={self.api_key}&address={address}'
        response = requests.get(url)
        result = json.loads(response.text)['result']
        return result

    def run_get_address(self, address):
        url = f'{self.api_base_url}getAddressInformation?api_key={self.api_key}&address={address}'
        response = requests.get(url)
        result = json.loads(response.text)['result']
        return result


    def _post(self, api_method, data=None, smc_addr=None, smc_method=None, stack=None):
        try:
            url = f'{self.api_base_url}{api_method}?api_key={self.api_key}'
            data = data or {
                'address': smc_addr,
                'method': smc_method,
                'stack': stack or []
            }

            response = requests.post(url, json=data)
            if not response.ok:
                raise Exception(response.status_code)

            response = json.loads(response.text)

            if response.get('result', None):
                result = response['result']
                success = (result.get('@type', 'ok') == 'ok') and \
                          (result.get('exit_code', 0) in [0, 1])
                if not success:
                    raise Exception(result)

                return result

            raise Exception(response['error'])

        except Exception as err:
            print('ERROR: ', err)
            raise
