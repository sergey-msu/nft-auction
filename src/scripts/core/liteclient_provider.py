import tempfile
from subprocess import check_output


class LiteclientProvider:
    def __init__(self, liteclient_path, config_path, wait_sec, wait_max_iters):
        self.liteclient_path = liteclient_path
        self.config_path = config_path
        self.wait_sec = wait_sec
        self.wait_max_iters = wait_max_iters
        self.current_seqnos = {}


    def send_boc(self, boc_b64):        
        with tempfile.TemporaryFile() as tmp:
            tmp.write(boc_b64)
            return self.send_boc_file(tmp.name)


    def send_boc_file(self, boc_file):
        result = check_output([self.liteclient_path, '-C', self.config_path, '-c', f'"sendfile {boc_file}"'])
        return result


    def run_get(self, smc_addr, smc_method, stack=None):
        print([self.liteclient_path, '-C', self.config_path, '-c', f'"runmethod {smc_addr} {smc_method}"'])
        result = check_output([self.liteclient_path, '-C', self.config_path, '-c', f'"runmethod {smc_addr} {smc_method}"'])
        return result
