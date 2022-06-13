from pickle import BUILD
import time
import yaml
from pkg_resources import resource_filename
from pprint import pprint, pformat

from dash import Dash, ctx
from dash.dependencies import Input, Output, State

from demo.consts import *
from demo.layout import layout
from demo.core.wallet import Wallet
from demo.core.nft_collection import NftCollection
from demo.core.nft_item import NftItem
from demo.core.nft_auction import NftAuction


# init Dash

with open(resource_filename(__name__, "configs/demo.yaml"), "r") as f:
    config = yaml.safe_load(f)
    
app = Dash(__name__)
app.layout = layout


# Callbacks

@app.callback(
    [Output('deadline-input', 'value')],
     Input('now-btn', 'n_clicks'))
def deploy_new_collection(n_clicks):
    return [int(time.time())  if n_clicks is not None else '']


@app.callback(
    [Output('coll-addr-link', 'children'), 
     Output('coll-addr-link', 'href'),
     Output('coll-addr-input', 'value')],
     Input('deploy-coll-btn', 'n_clicks'))
def deploy_new_collection(n_clicks):
    if n_clicks is None:
        return ['', '', '']

    print('Deploying collection...')

    seed = int(1000*time.time())
    wallet = Wallet(BUILDER, API, address=WALLET1, pk_file=PRIVATE_KEY)
    collection = NftCollection(BUILDER, API, wallet)
    config = {
      'collection_content_uri': f'https://myorg.com/collection{seed}.json',
      'item_content_base_uri':  'https://myorg.com/',
      'royalty_base':    100,
      'royalty_factor':  5,   # 5% royalty
      'coll_init_ng':    INIT_NG,
      'owner_address':   COLL_OWNER_ADDR,
      'royalty_address': ROYALTY_ADDR,
    }
    collection.from_config(config)
    collection.deploy(send=True)

    address = collection.address

    print(f'\nCollection address: {address}\n')

    return [address, SANDBOX.format(addr=address), address]


@app.callback(
    [Output('item-addr-link', 'children'), 
     Output('item-addr-link', 'href'),
     Output('item-addr-input', 'value')],
     Input('mint-item-btn', 'n_clicks'),
     State('coll-addr-input', 'value'))
def mint_new_item(n_clicks, value):
    if n_clicks is None:
        return ['', '', '']

    print('Minting NFT item...')

    collection = NftCollection(BUILDER, API, address=value)
    result = collection.get_collection_data()
    index = result['next_item_index']

    wallet = Wallet(BUILDER, API, address=WALLET1, pk_file=PRIVATE_KEY)
    config = {
        'owner_address': COLL_OWNER_ADDR,
        'item_index': index,
        'coll_ng': COLL_NG,
        'item_ng': INIT_NG,
        'item_content_uri': 'item?filename=harold.jpg',
    }
    item = NftItem(BUILDER, API, collection, wallet)
    item.from_config(config)
    item.mint(send=True)

    address = item.address

    print(f'\nNFT item address: {address}\n')

    return [address, SANDBOX.format(addr=address), address]


@app.callback(
    [Output('auction-addr-link', 'children'), 
     Output('auction-addr-link', 'href'), 
     Output('auction-addr-input', 'value')],
    Input('deploy-auction-btn', 'n_clicks'),
    [State('item-addr-input', 'value'), 
     State('market-fee-addr-input', 'value'),
     State('market-fee-input', 'value'),
     State('royalty-addr-input', 'value'),
     State('royalty-input', 'value'),
     State('deadline-input', 'value'),
     State('sniper-before-input', 'value'),
     State('sniper-prolong-input', 'value'),
     State('min-bid-input', 'value'),
     State('max-bid-input', 'value'),
     State('bid-step-input', 'value')],
    prevent_initial_call=True)
def deploy_new_auction(n_clicks, 
                       item_addr, 
                       market_fee_addr, market_fee_pct, royalty_addr, royalty_pct,
                       auction_deadline, sniper_before, sniper_prolong,
                       min_bid, max_bid, bid_step):
    print('Deploying auction...')

    max_bid = max_bid or None
    if max_bid:
        max_bid = int(10**9 * float(max_bid))
        if (max_bid <= min_bid):
            max_bid = None

    sniper_before = sniper_before or None
    if sniper_before:
        sniper_before = int(sniper_before)

    sniper_prolong = sniper_prolong or None
    if sniper_prolong:
        sniper_prolong = int(sniper_prolong)

    market_fee_pct = float(market_fee_pct)
    if market_fee_pct < 0 or market_fee_pct > 100:
        raise ValueError('market_fee_pct')

    royalty_pct = float(royalty_pct)
    if royalty_pct < 0 or royalty_pct > 100:
        raise ValueError('royalty_pct')

    wallet = Wallet(BUILDER, API, address=WALLET1, pk_file=PRIVATE_KEY)
    auction = NftAuction(BUILDER, API, wallet)
    config = {
      'marketplace_address': MARKETPLACE,
      'nft_address': item_addr,
      'marketplace_fee_address': market_fee_addr,
      'marketplace_fee_numer': int(market_fee_pct*100),
      'marketplace_fee_denom': 10000,
      'royalty_address': royalty_addr,
      'royalty_numer': int(royalty_pct*100),
      'royalty_denom': 10000,
      'auction_finish_time': int(auction_deadline) if auction_deadline else None,
      'auction_salt': int(time.time()),
      'sniper_before_time': sniper_before,
      'sniper_after_prolong': sniper_prolong,
      'min_bid': int(10**9 * float(min_bid)),
      'max_bid': max_bid,
      'bid_step': int(10**9 * float(bid_step)),
      'auction_init_ng': INIT_NG,
    }
    auction.from_config(config)
    auction.deploy(send=True)

    pprint(config)

    address = auction.address

    print(f'\nAuction address: {address}\n')

    return [address, SANDBOX.format(addr=address), address]


@app.callback(
    [Output('r-item-addr-label', 'children'),
     Output('r-item-addr-label', 'href'),
     Output('r-item-owner-addr-label', 'children'),
     Output('r-item-owner-addr-label', 'href'),
     Output('r-auc-item-owner-addr-label', 'children'),
     Output('r-auc-item-owner-addr-label', 'href'),
     Output('r-auc-curr-winner-addr-label', 'children'),
     Output('r-auc-curr-winner-addr-label', 'href'),
     Output('r-auc-curr-winner-bid-label', 'children'),
     Output('r-auc-is-started-label', 'children'),
     Output('r-auc-is-finished-label', 'children'),
     Output('r-auc-is-cancelled-label', 'children'),
     Output('r-auc-curr-time-label', 'children'),],
    Input('info-auction-btn', 'n_clicks'),
    State('auction-addr-input', 'value'),
    prevent_initial_call=True)
def auction_info(n_clicks, auction_addr):
    print('Fetching auction info...')

    auction = NftAuction(BUILDER, API, address=auction_addr)
    nft_address = auction.get_general_data()['nft_address']

    item = NftItem(BUILDER, API, address=nft_address)

    general_result = auction.get_general_data()
    auction_result = auction.get_auction_data()
    nft_result = item.get_nft_data()

    nft_address = general_result['nft_address'] or '-'
    nft_address_href = SANDBOX.format(addr=nft_address) if nft_address != '-' else ''

    owner_address = nft_result['owner_address'] or '-'
    owner_address_href = SANDBOX.format(addr=owner_address) if owner_address != '-' else ''

    nft_owner_address = general_result['nft_owner_address'] or '-'
    nft_owner_address_href = SANDBOX.format(addr=nft_owner_address) if nft_owner_address != '-' else ''

    curr_winner_address = auction_result['curr_winner_address'] or '-'
    curr_winner_address_href = SANDBOX.format(addr=curr_winner_address) if curr_winner_address != '-' else ''

    return [
        nft_address, nft_address_href,
        owner_address, owner_address_href,
        nft_owner_address, nft_owner_address_href,    
        curr_winner_address, curr_winner_address_href,
        auction_result['curr_winner_bid'],
        str(general_result['nft_owner_address'] is not None),
        str(auction_result['is_finished']),
        str(auction_result['is_cancelled']), 
        auction_result['auction_current_time'],
    ]


@app.callback(
    Output('message-label', 'children'),
    Input('start-auction-btn', 'n_clicks'),
    Input('cancel-auction-btn', 'n_clicks'),
    Input('finish-auction-btn', 'n_clicks'),
    Input('bid-auction-btn', 'n_clicks'),
    [State('auction-addr-input', 'value'),
     State('bidder-addr-input', 'value'),
     State('bidder-bid-input', 'value')],
    prevent_initial_call=True
)
def update_graph(n1, n2, n3, n4, auction_addr, bidder_addr=None, bidder_bid=None):
    triggered_id = ctx.triggered_id
    print(triggered_id)
    if triggered_id == 'start-auction-btn':
         return auction_start(auction_addr)
    if triggered_id == 'cancel-auction-btn':
         return auction_cancel(auction_addr)
    if triggered_id == 'finish-auction-btn':
         return auction_finish(auction_addr)
    if triggered_id == 'bid-auction-btn':
         return auction_bid(auction_addr, bidder_addr, bidder_bid)


def auction_start(auction_addr):
    print('Starting auction...')

    try:
        wallet = Wallet(BUILDER, API, address=WALLET1, pk_file=PRIVATE_KEY)
        auction = NftAuction(BUILDER, API, address=auction_addr)
        nft_address = auction.get_general_data()['nft_address']

        item = NftItem(BUILDER, API, wallet=wallet, address=nft_address)
        item.transfer_ownership(new_owner_address=auction_addr, 
                                forward_amount=INIT_NG,
                                item_ng=START_NG, send=True)

        msg = 'Auction START request sended. Wait ~20 sec and press Info'
    except Exception as ex:
        msg = ex.message

    return [msg]


def auction_cancel(auction_addr):
    print('Cancelling auction...')

    try:
        wallet = Wallet(BUILDER, API, address=WALLET1, pk_file=PRIVATE_KEY)
        auction = NftAuction(BUILDER, API, address=auction_addr, wallet=wallet)
        auction.cancel(cancel_ng=CANCEL_NG, send=True)

        msg = 'Auction CANCEL request sended. Wait ~20 sec and press Info'
    except Exception as ex:
        msg = ex.message

    return [msg]



def auction_finish( auction_addr):
    print('Finishing auction...')

    try:
        wallet = Wallet(BUILDER, API, address=WALLET1, pk_file=PRIVATE_KEY)
        auction = NftAuction(BUILDER, API, address=auction_addr, wallet=wallet)
        auction.finish(finish_ng=FINISH_NG, send=True)

        msg = 'Auction FINISH request sended. Wait ~20 sec and press Info'
    except Exception as ex:
        msg = ex.message

    return [msg]


def auction_bid(auction_addr, bidder_addr, amount):
    print('Place a bid...')

    try:
        amount = int(10**9 * float(amount))
        if amount > 10_000_000_000:
            raise ValueError('Bid is too much for testing')

        bidder = Wallet(BUILDER, API, address=bidder_addr, pk_file=PRIVATE_KEY)
        bidder.transfer_money(to=auction_addr, amount=amount, send=True)

        msg = 'Bid placed. Wait ~20 sec and press Info'
    except Exception as ex:
        msg = ex.message

    return [msg]


if __name__ == '__main__':
    app.run_server(**config['server'])
