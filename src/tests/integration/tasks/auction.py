import yaml
from pprint import pprint

from tests.integration.core.builder import Builder
from tests.integration.core.http_api_provider import HttpApiProvider
from tests.integration.core.wallet import Wallet
from tests.integration.core.nft_auction import NftAuction
from tests.integration.core.nft_item import NftItem


builder = None
api = None


def init():
  with open('tests/integration/configs/app.yaml') as f:
      config = yaml.safe_load(f)

  global builder
  builder = Builder(**config['core'])
  builder.compile_sources(**config['compile'])
  builder.build_templates(**config['compile'])

  global api
  api = HttpApiProvider(**config['api'])


def deploy(seed,
           wallet_addr, market_addr, item_addr, 
           market_num=10, market_den=100, 
           royalty_addr=None, send=True,
           royalty_num=5, royalty_den=100,
           auc_fin=None, snip_before=5, snip_after=10,
           min_bid=1_000_000_000, max_bid=5_000_000_000, bid_step=500_000_000,
           init_ng=55_000_000,
           private_key='wallet.pk', **kwargs):
    print('Deploying new auction...')

    wallet = Wallet(builder, api, address=wallet_addr, pk_file=private_key)

    auction = NftAuction(builder, api, wallet)
    config = {
      'marketplace_address': market_addr,
      'nft_address': item_addr,
      'marketplace_fee_address': market_addr,
      'marketplace_fee_numer': market_num,
      'marketplace_fee_denom': market_den,
      'royalty_address': royalty_addr or wallet_addr,
      'royalty_numer': royalty_num,
      'royalty_denom': royalty_den,
      'auction_finish_time': auc_fin,
      'auction_salt': int(seed), # int(time.time()),
      'sniper_before_time': snip_before,
      'sniper_after_prolong': snip_after,
      'min_bid':   min_bid,
      'max_bid': max_bid,
      'bid_step':   bid_step,
      'auction_init_ng': init_ng,
    }
    auction.from_config(config)
    auction.deploy(send=send)

    print(f'\nAuction address: {auction.address}\n')


def start(addr, wallet_addr, item_ng=80_000_000, forw_ng=50_000_000, private_key='wallet.pk', send=True, **kwargs):
    print('Starting auction...')

    wallet = Wallet(builder, api, address=wallet_addr, pk_file=private_key)
    auction = NftAuction(builder, api, address=addr)

    nft_address = auction.get_general_data()['nft_address']

    item = NftItem(builder, api, wallet=wallet, address=nft_address)
    item.transfer_ownership(new_owner_address=addr, 
                            forward_amount=forw_ng,
                            item_ng=item_ng, send=send)


def cancel(addr, wallet_addr, cancel_ng=150_000_000, private_key='wallet.pk', send=True, **kwargs):
    print('Cancelling auction...')

    wallet = Wallet(builder, api, address=wallet_addr, pk_file=private_key)
    auction = NftAuction(builder, api, address=addr, wallet=wallet)

    auction.cancel(cancel_ng=cancel_ng, send=send)


def finish(addr, wallet_addr, finish_ng=150_000_000, private_key='wallet.pk', send=True, **kwargs):
    print('Cancelling auction...')

    wallet = Wallet(builder, api, address=wallet_addr, pk_file=private_key)
    auction = NftAuction(builder, api, address=addr, wallet=wallet)
    auction.finish(finish_ng=finish_ng, send=send)


def bid(addr, amount, bidder_addr, bidder_pk='wallet.pk', send=True, **kwargs):
    print('Make a bid...')

    bidder = Wallet(builder, api, address=bidder_addr, pk_file=bidder_pk)
    bidder.transfer_money(to=addr, amount=amount, send=send)


def info(addr, **kwargs):
    auction = NftAuction(builder, api, address=addr)
    nft_address = auction.get_general_data()['nft_address']

    item = NftItem(builder, api, address=nft_address)

    print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: MARKETPLACE FEE DATA >>>>>>>>>>>>>>>>>>>>>>>>')
    result = auction.get_marketplace_fee_data()
    pprint(result)

    print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ROYALTY DATA >>>>>>>>>>>>>>>>>>>>>>>>')
    result = auction.get_royalty_data()
    pprint(result)

    print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: GENERAL DATA >>>>>>>>>>>>>>>>>>>>>>>>')
    result = auction.get_general_data()
    pprint(result)

    print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: AUCTION DATA >>>>>>>>>>>>>>>>>>>>>>>>')
    result = auction.get_auction_data()
    pprint(result)

    print('\n>>>>>>>>>>>>>>>>>>>>>>>> GET: ITEM DATA >>>>>>>>>>>>>>>>>>>>>>>>')
    result = item.get_nft_data()
    pprint(result)



def run_auction(command, **kwargs):
    init()

    if command == 'new':
        deploy(**kwargs)
    elif command == 'start':
        start(**kwargs)
    elif command == 'cancel':
        cancel(**kwargs)
    elif command == 'finish':
        finish(**kwargs)
    elif command == 'info':
        info(**kwargs)
    elif command == 'bid':
        bid(**kwargs)
    else:
      raise Exception(f'Unknown command {command}')
