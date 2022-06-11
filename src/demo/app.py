import time
import yaml
from pkg_resources import resource_filename

from dash import Dash
from dash.dependencies import Input, Output, State

from demo.consts import *
from demo.layout import layout
from demo.core.wallet import Wallet
from demo.core.nft_collection import NftCollection
from demo.core.nft_item import NftItem


# init Dash

with open(resource_filename(__name__, "configs/demo.yaml"), "r") as f:
    config = yaml.safe_load(f)
    
app = Dash(__name__)
app.layout = layout


# Callbacks

@app.callback(
    [Output('coll-addr-link', 'children'), 
     Output('coll-addr-link', 'href'),
     Output('coll-addr-input', 'value')],
     Input('deploy-coll-btn', 'n_clicks'))
def deploy_new_collection(n_clicks):
    if n_clicks is None:
        return ['', '', '']

    print('Deploying collection...')

    seed = int(10*time.time())
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
     Output('item-addr-link', 'href')],
     Output('item-addr-input', 'value'),
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


if __name__ == '__main__':
    app.run_server(**config['server'])
