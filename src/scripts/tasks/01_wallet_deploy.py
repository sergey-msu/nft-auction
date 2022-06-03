import sys
import yaml

from core.builder import Builder
from core.api_provider_factory import ApiProviderFactory
from contracts.wallet import Wallet


# at first run ./deploy-sign-provider.sh [n] 0
# the out/new-provider-query.boc file will appear

def main():
    with open('configs/app.yaml') as f:
        config = yaml.safe_load(f)

    builder = Builder(**config['core'])
    api = ApiProviderFactory.create(config['api'])

    builder.clear_out()
    builder.compile_sources(**config['compile'])
    builder.build_templates(**config['compile'])


    seed_id=int(sys.argv[1])
    send = bool(int(sys.argv[2]))
    generate_private_key = int(sys.argv[3])
    pk_file = sys.argv[4] if len(sys.argv) > 4 else 'wallet.pk'

    # 1. find out wallet address
    wallet = Wallet(builder, api, pk_file=pk_file, user=90)
    wallet.deploy(seed_id, generate_private_key=generate_private_key, wc="0", send=False)

    print(f'\nWallet address: {wallet.address}\n')

    # 2. send money to address: TODO from outside

    # 3. deploy smc for a new wallet
    if send:
      wallet.deploy(seed_id, generate_private_key=0, wc="0", send=True)

    # 4. get seqno
    print('seqno:', wallet.seqno())

if __name__ == '__main__':
    main()
