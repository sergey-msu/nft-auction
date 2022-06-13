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
                              style={'text-overflow': 'ellipsis', 
                                     'overflow': 'hidden', 
                                     'white-space': 'nowrap', 
                                     'white-space': 'nowrap'})], 
                 href=SANDBOX.format(addr=link), 
                 target='_blank'),
    ], style={'padding': '10px 0'})


def exit_code_tr(code, text, details):
    return html.Tr([
                    html.Td(code, style={'font-weight': 'bold'}), 
                    html.Td(text, style={'font-size': '10pt', 'padding': '4px'})
            ], title=details)


def get_result_tr(label, id):
    return html.Tr([html.Td(label, style={'text-align': 'right'}), 
                    html.Td('', id=id, style={'text-align': 'left'}),
            ])


def get_result_link_tr(label, id, value, href):
    return html.Tr([html.Td(label, style={'text-align': 'right'}), 
                    dcc.Link(id=id, children=value, href=href, target='_blank', style={}),
            ])


def get_auction_param_tr(label, id, placeholder=None, width=400, value='', pattern=None, align='center', after=None):
    value_td = [dcc.Input(id=id, value=value, type='text', placeholder=placeholder or label.lower(),
                            pattern=pattern,
                            style={'width': f'{width}px',
                                    'height': '25px',
                                    'text-align': 'center',
                                    'margin': '0 10px'})]
    if after:
        value_td.append(after)

    return html.Tr([html.Td(label, style={'text-align': 'right'}), 
                    html.Td(value_td, style={'text-align': align})
            ])


def get_auction_deadline_param_tr(label, id, placeholder=None, width=400, value='', pattern=None):
    return html.Tr([html.Td(label, style={'text-align': 'right'}), 
                    html.Td([
                        dcc.Input(id=id, value=value, type='text', placeholder=placeholder or label.lower(),
                                  pattern=pattern,
                                  style={'width': f'{width}px',
                                         'height': '25px',
                                         'text-align': 'center',
                                         'margin': '0 10px'}),
                        html.Button('now', id='now-btn', 
                                     style={'text-decoration': 'underline',
                                            'background': 'none',
                                            'border': 'none',
                                            'padding': '0!important',
                                            'color': 'blueviolet',
                                            'cursor': 'pointer'}),
                    ])
            ])


# main header
header = html.Div([
        html.H1(id='H1', children=[
            html.Div('TON Auction Demo'),
            dcc.Link(children='github', 
                    href='https://github.com/sergey-msu/nft-auction', 
                    target='_blank', style={'font-size': '8pt', 
                                            'float': 'right',
                                            'margin': '20px',
                                            'color': 'cornflowerblue'}),
            ], 
            style = {'textAlign':'center',
                        'color':'white',
                        'fontFamily': 'Helvetica',
                        'paddingTop':40, 
                        'paddingBottom':40, 
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
        style={'margin': '30px 0 10px 0'}),
        
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
            style={}
        )
    ], 
    style = {'width': '20%', 'height': '200vh', 'float': 'left', 'background': '#b9deff', 'padding': '20px'}
)

# collection operations
collection_div = html.Div([
        html.Label(children='Collection', style={'padding': '0 0 20px 0', 'font-weight': 'bold', 'font-size': 'larger'}),
        html.Div(style={'margin': '10px'}),
        html.Button('Deploy New', id='deploy-coll-btn', className='btn',
                    style={'width': '110px',
                            'height': '30px',
                            'borderRadius': '15px 15px',
                            'border-width': '3',
                            'margin': '0 10px',
                            'color': 'white'}),
        html.Div(style={'margin': '5px'}),
        dcc.Link(id='coll-addr-link', children='', href='link', target='_blank', style={}),
    ], style={'padding': '0 0 25px 0'})

# item operations
item_div = html.Div([
        html.Label(children='NFT', style={'padding': '0 0 20px 0', 'font-weight': 'bold', 'font-size': 'larger'}),
        html.Div(style={'margin': '10px'}),

        html.Table(
            html.Tbody([
                get_auction_param_tr('Collection Address', 'coll-addr-input', pattern='^.{48}$'),
            ]),
            style={'margin-left': 'auto', 'margin-right': 'auto', 'padding-right': '120px'}
        ),
        html.Div(style={'margin': '5px'}),
        html.Button('Mint New', id='mint-item-btn', className='btn',
                    style={'width': '110px',
                            'height': '30px',
                            'borderRadius': '15px 15px',
                            'borderWidth': '3',
                            'margin': '0 10px',
                            'color': 'white'}),
        html.Div(style={'margin': '5px'}),
        dcc.Link(id='item-addr-link', children='', href='link', target='_blank', style={}),
    ], style={'padding': '0 0 25px 0'})

# auction operations
auction_div = html.Div([
        html.Label(children='Auction', style={'padding': '0 0 20px 0', 'font-weight': 'bold', 'font-size': 'larger'}),
        html.Div(style={'margin': '10px'}),
        
        html.Table(
            html.Tbody([
                get_auction_param_tr('NFT Address', 'item-addr-input', placeholder='item address', pattern='^.{48}$'),
                get_auction_param_tr('Marketplace Fee Address', 'market-fee-addr-input', value=WALLET2, pattern='^.{48}$'),
                get_auction_param_tr('Royalty Address', 'royalty-addr-input', value=WALLET3, pattern='^.{48}$'),
            ]),
            style={'margin-left': 'auto', 'margin-right': 'auto', 'padding-right': '150px'}
        ),
        html.Div(style={'margin': '5px'}),

        html.Table(
            html.Tbody([
                get_auction_param_tr('Market fee, %', 'market-fee-input', placeholder='fee, %', value=5, width=40, pattern='^(\d+(\.\d+)?)$'),
                get_auction_param_tr('Royalty, %', 'royalty-input', placeholder='fee, %', width=40, value=7, pattern='^(\d+(\.\d+)?)$'),
                get_auction_deadline_param_tr('Auction Deadline, sec', 'deadline-input', placeholder='unix time, sec', width=100, pattern='^(\d+)$'),
                get_auction_param_tr('Sniper before, sec', 'sniper-before-input', placeholder='sec', value=300, width=40, pattern='^(\d+)$'),
                get_auction_param_tr('Sniper prolong, sec', 'sniper-prolong-input', placeholder='sec', value=600, width=40, pattern='^(\d+)$'),
                get_auction_param_tr('Min bid, TON', 'min-bid-input', placeholder='TON', value=1, width=40, pattern='^(\d+(\.\d+)?)$'),
                get_auction_param_tr('Max bid, TON', 'max-bid-input', placeholder='TON', width=40, pattern='^(\d+(\.\d+)?)$'),
                get_auction_param_tr('Bid step, TON', 'bid-step-input', placeholder='TON', value=0.1, width=40, pattern='^(\d+(\.\d+)?)$'),
            ]),
            style={'margin-left': 'auto', 'margin-right': 'auto', 'padding-right': '150px'}
        ),
        
        html.Div(style={'margin': '5px'}),
        html.Button('Deploy New', id='deploy-auction-btn', className='btn',
                    style={'width': '110px',
                            'height': '30px',
                            'borderRadius': '15px 15px',
                            'borderWidth': '3',
                            'margin': '0 10px',
                            'color': 'white'}),
        html.Div(style={'margin': '5px'}),
        dcc.Link(id='auction-addr-link', children='', href='link', target='_blank', style={}),
        
    ], style={'padding': '0 0 25px 0'})


# auction actions
fun_div = html.Div([
        html.Label(children='Have Fun', style={'padding': '0 0 20px 0', 'font-weight': 'bold', 'font-size': 'larger'}),
        html.Div(style={'margin': '10px'}),

        html.Table(
            html.Tbody([
                get_auction_param_tr('Auction Address', 'auction-addr-input', pattern='^.{48}$'),
                get_auction_param_tr('Bidder Address', 'bidder-addr-input', pattern='^.{48}$'),
            ]),
            style={'margin-left': 'auto', 'margin-right': 'auto', 'padding-right': '100px'}
        ),
        html.Table(
            html.Tbody([
                get_auction_param_tr('Bid', 'bidder-bid-input', pattern='^(\d+(\.\d+)?)$', placeholder='TON', width=40, align='left',
                    after=html.Button(children='1', id='bid-auction-btn', className='ton-btn',
                                      title='Place a bid',
                                      style={'height': '35px', 'width': '35px', 'border-radius': '18px', 'color': 'transparent'})
                ),
            ]),
            style={'margin-left': 'auto', 'margin-right': 'auto', 'padding-right': '0px'}
        ),

        html.Div(style={'margin': '20px'}),
        html.Button('Info', id='info-auction-btn', className='grey-btn',
                    style={'width': '110px',
                            'height': '30px',
                            'borderRadius': '15px 15px',
                            'borderWidth': '3',
                            'margin': '0 10px',
                            'color': 'white'}),
        html.Button('Start', id='start-auction-btn', className='green-btn',
                    style={'width': '110px',
                            'height': '30px',
                            'borderRadius': '15px 15px',
                            'borderWidth': '3',
                            'margin': '0 10px',
                            'color': 'white'}),
        html.Button('Cancel', id='cancel-auction-btn', className='yellow-btn',
                    style={'width': '110px',
                            'height': '30px',
                            'borderRadius': '15px 15px',
                            'borderWidth': '3',
                            'margin': '0 10px',
                            'color': 'white'}),
        html.Button('Finish', id='finish-auction-btn', className='red-btn',
                    style={'width': '110px',
                            'height': '30px',
                            'borderRadius': '15px 15px',
                            'borderWidth': '3',
                            'margin': '0 10px',
                            'color': 'white'}),

        html.Div(style={'margin': '30px'}),
        html.Label(id='message-label', style={'font-size': '12pt', 'color': 'blue'}),

        html.Div(style={'margin': '30px'}),
        html.Table(
            html.Tbody([
                get_result_link_tr('NFT:', 'r-item-addr-label', '', ''),
                get_result_link_tr('Current NFT Owner:', 'r-item-owner-addr-label', '', ''),
                get_result_link_tr('Auction NFT Owner:', 'r-auc-item-owner-addr-label', '', ''),
                get_result_link_tr('Auction Curr Bid From:', 'r-auc-curr-winner-addr-label', '', ''),
                get_result_tr('Auction Curr Bid:', 'r-auc-curr-winner-bid-label'),
                get_result_tr('Auction is Started:', 'r-auc-is-started-label'),
                get_result_tr('Auction is Finished:', 'r-auc-is-finished-label'),
                get_result_tr('Auction is Cancelled:', 'r-auc-is-cancelled-label'),
                get_result_tr('Auction Time:', 'r-auc-curr-time-label'),
            ]),
            style={'margin-left': 'auto', 'margin-right': 'auto', 'padding-right': '100px'}
        ),
    ], style={'padding': '0 0 25px 0'})


# working panel
right_panel = \
    html.Div([
        collection_div,
        item_div,
        auction_div,
        fun_div,
    ], style={'text-align': 'center', 'padding': '20px 0'})

layout = html.Div([header, html.Div([left_panel, right_panel])], style={'fontFamily': 'Helvetica',})
