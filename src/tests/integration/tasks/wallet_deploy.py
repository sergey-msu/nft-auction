import sys
from core.wallet import Wallet
from tasks.consts import builder, api


def main():
    # 0. args
    seed_id=int(sys.argv[1])
    send = bool(int(sys.argv[2]))
    generate_private_key = int(sys.argv[3])
    pk_file = sys.argv[4] if len(sys.argv) > 4 else 'wallet.pk'

    # 1. find out wallet address
    wallet = Wallet(builder, api, pk_file=pk_file)
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
