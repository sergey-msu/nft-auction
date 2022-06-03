import yaml

from core.builder import Builder
from core.api_provider_factory import ApiProviderFactory
from scripts.contracts.snft_provider import SnftProvider


def main():
    with open('configs/app.yaml') as f:
        config = yaml.safe_load(f)

    builder = Builder(**config['core'])
    api = ApiProviderFactory.create(config['api'])

    builder.clear_out()
    builder.compile_sources(**config['compile'])
    builder.build_templates(**config['compile'])

    sign_provider = SnftProvider(builder, api, 
                                 address=config['core']['sign_provider_address'],
                                 pk_file=config['core']['sign_provider_pk'],
                                 user=0)
    sign_provider.transfer_money(to='kQAWYHnDf8qmG9mC1CGD1Svf9_9OjWpDgL9EU2fgsTrfHyNM', 
                                 amount=19091984,
                                 send=True)

    # if API not working: /opt/liteclient-build/lite-client/lite-client -C /opt/liteclient-build/testnet-global.config.json -c "sendfile /home/sergey/Work/proj/blockchain/ton.era/nft-signable/out/0/wallet-transfer-money-query.boc"


if __name__ == '__main__':
    main()
