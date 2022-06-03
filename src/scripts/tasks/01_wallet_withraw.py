import yaml

from core.builder import Builder
from core.api_provider_factory import ApiProviderFactory
from contracts.wallet import Wallet


def main():
    with open('configs/app.yaml') as f:
        config = yaml.safe_load(f)

    builder = Builder(**config['core'])
    api = ApiProviderFactory.create(config['api'])

    builder.clear_out()
    builder.compile_sources(**config['compile'])
    builder.build_templates(**config['compile'])

    wallet = Wallet(builder, api,
                    address='EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs',
                    pk_file='wallet.pk',
                    user=91)
    wallet.transfer_money(to='EQB1grTB2NIAbshA8C1Fu8EiSHiY_ZbTE-tRneTMKgdHAUJH', 
                          amount=7_000_000_000,
                          send=True)

    # if API not working: /opt/liteclient-build/lite-client/lite-client -C /opt/liteclient-build/testnet-global.config.json -c "sendfile /home/sergey/Work/proj/blockchain/ton.era/nft-signable/out/0/wallet-transfer-money-query.boc"


if __name__ == '__main__':
    main()
