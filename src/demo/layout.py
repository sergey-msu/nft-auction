from dash import dcc, html

from demo.consts import *


def get_link_div(title, id, link):
    return html.Div(
    [
        html.Label(children=f'{title}:'),
        html.Br(),
        dcc.Link(id=id, 
                 children=[
                     html.Div(children=link,
                              style={'font-size': 'small', 
                                     'text-overflow': 'ellipsis', 
                                     'overflow': 'hidden', 
                                     'white-space': 'nowrap', 
                                     'white-space': 'nowrap'})], 
                 href=SANDBOX.format(addr=link), 
                 target='_blank'),
    ], style={'padding': '10px 0'})


def exit_code_tr(code, text, details):
    return html.Tr([
                    html.Td(code, style={'font-weight': 'bold'}), 
                    html.Td(text, style={'font-size': '9pt'})
            ], title=details)


# main header
header = html.Div([
        html.H1(id='H1', children=[
            html.Div('TON Auction Demo'),
            dcc.Link(children='github', 
                    href='https://github.com/sergey-msu/nft-auction', 
                    target='_blank', style={'font-size': '8pt'}),
            ], 
            style = {'textAlign':'center',
                        'color':'white',
                        'fontFamily': 'Helvetica',
                        'paddingTop':40, 
                        'paddingBottom':5, 
                        'margin-block-end': 0,
                        'margin-inline-start': 0,
                        'background': 'linear-gradient(0.25turn, #456bf8, #1b2a63)'}),
    ])

# panel with constants
left_panel = html.Div(
    [
        get_link_div('Marketplace', 'market-addr-link', MARKETPLACE),
        get_link_div('Wallet #1', 'wallet1-addr-link', WALLET1),
        get_link_div('Wallet #2', 'wallet2-addr-link', WALLET2),
        get_link_div('Wallet #3', 'wallet3-addr-link', WALLET3),

        html.Div([
            html.Label(children='TVM Exit Codes:'),
            html.Br()], 
        style={'margin': '30px 0 0 0'}),
        
        html.Table(
            html.Tbody([
                exit_code_tr('447', 'msg_value < min_gas', 'Message gas safeguard violation. Should be `msg_value >= min_gas_amount()`'),
                exit_code_tr('450', 'bid < min_bid', 'Trying to make a bid less than a `min_bid`. Should be `msg_value >= min_bid_value + min_gas_amount()`'),
                exit_code_tr('458', 'wrong cancel addr', 'Trying to cancel auction from address different from `nft_address` of `marketplace_address`'),
                exit_code_tr('478', 'wrong finish addr', 'Trying to finish auction from address different from `nft_address` (before deadine)'),
                exit_code_tr('500', 'contract uninitialized', 'Trying to make a first call to uninitialized auction from address different from `nft_address`'),
                exit_code_tr('501', 'wrong init op code', 'Trying to make a first call to uninitialized auction with wrong operation code'),
                exit_code_tr('600', 'already finished', 'Trying to finish or cancel auction that already finished'),
                exit_code_tr('800', 'finish insufficient balance', 'Trying to finish auction with insufficient balance. Should be: `my_balance > min_gas_amount() + min_tons_for_storage() + transfer_invoke_fee() + fwd_fee`'),
                exit_code_tr('801', 'finish insufficient balance', 'the same as 800 but in case of existing bidder. Auction balance should be: `my_balance > royalty_amount + marketplace_fee + min_gas_amount() + min_tons_for_storage() + transfer_invoke_fee() + 4*fwd_fee`'),
                exit_code_tr('810', 'cancel insufficient balance', 'trying to cancel auction with insufficient balance. Should be: `my_balance > min_gas_amount() + min_tons_for_storage() + transfer_invoke_fee() + fwd_fee`'),
                exit_code_tr('811', 'cancel insufficient balance', 'the same as 810 but in case of existing bidder. Auction balance should be: `my_balance > min_gas_amount() + min_tons_for_storage() + transfer_invoke_fee() + 2*fwd_fee`'),
            ]),
        style={'font-size': 'small'})
    ], 
    style = {'width': '20%', 'height': '500px', 'float': 'left', 'background': '#C5D0F8', 'padding': '20px'}
)

# collection operations
collection_div = html.Div([
        html.Label(children='Collection', style={'padding': '0 0 20px 0'}),
        html.Div(style={'margin': '10px'}),
        html.Button('Deploy New', id='deploy-coll-btn',
                    style={'width': '110px',
                            'height': '30px',
                            'borderRadius': '15px 15px',
                            'borderWidth': '3',
                            'margin': '0 10px',
                            'backgroundColor': '#0088cc',
                            'color': 'white'}),
        html.Div(style={'margin': '5px'}),
        dcc.Link(id='coll-addr-link', children='', href='link', target='_blank', style={'font-size': 'small'}),
    ], style={'padding': '0 0 25px 0'})

# item operations
item_div = html.Div([
        html.Label(children='NFT', style={'padding': '0 0 20px 0'}),
        html.Div(style={'margin': '10px'}),
        dcc.Input(id="coll-addr-input", type='text', placeholder="collection address",
                  style={'width': '400px',
                         'height': '25px',
                         'text-align': 'center',
                         'margin': '0 10px'}),
        html.Div(style={'margin': '5px'}),
        html.Button('Mint New', id='mint-item-btn',
                    style={'width': '110px',
                            'height': '30px',
                            'borderRadius': '15px 15px',
                            'borderWidth': '3',
                            'margin': '0 10px',
                            'backgroundColor': '#0088cc',
                            'color': 'white'}),
        html.Div(style={'margin': '5px'}),
        dcc.Link(id='item-addr-link', children='', href='link', target='_blank', style={'font-size': 'small'}),
    ], style={'padding': '0 0 25px 0'})

# auction operations
auction_div = html.Div([
        html.Label(children='Auction', style={'padding': '0 0 20px 0'}),
        html.Div(style={'margin': '10px'}),
        dcc.Input(id="item-addr-input", type='text', placeholder="NFT address",
                  style={'width': '400px',
                         'height': '25px',
                         'text-align': 'center',
                         'margin': '0 10px'}),
        html.Div(style={'margin': '5px'}),
        html.Button('Deploy New', id='deploy-auction-btn',
                    style={'width': '110px',
                            'height': '30px',
                            'borderRadius': '15px 15px',
                            'borderWidth': '3',
                            'margin': '0 10px',
                            'backgroundColor': '#0088cc',
                            'color': 'white'}),
        html.Div(style={'margin': '5px'}),
        dcc.Link(id='auction-addr-link', children='', href='link', target='_blank', style={'font-size': 'small'}),
    ], style={'padding': '0 0 25px 0'})

# working panel
right_panel = \
    html.Div([
        collection_div,
        item_div,
        auction_div,
    ], style={'text-align': 'center', 'padding': '20px'})

layout = html.Div([header, html.Div([left_panel, right_panel])], style={'fontFamily': 'Helvetica',})
