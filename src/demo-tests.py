import sys
import argparse
from tests.integration.tasks.auction import run_auction

from tests.integration.tasks.wallet import run_wallet
from tests.integration.tasks.marketplace import run_marketplace
from tests.integration.tasks.collection import run_collection
from tests.integration.tasks.item import run_item
from tests.integration.tasks.auction import run_auction


def get_wallet_args(subparsers):
    subparser = subparsers.add_parser('wallet')
    sub2parsers = subparser.add_subparsers()

    # deploy new wallet
    subparser = sub2parsers.add_parser('new')    
    subparser.add_argument(
        '-s', '--seed',
        help='Wallet seed',
        type=int,
        required=True)
    subparser.add_argument(
        '-g', '--generate_key',
        help='Generate new private key',
        type=int,
        default=0)
    subparser.add_argument(
        '-k', '--private_key',
        help='Private key file name',
        default='wallet.pk')
    subparser.add_argument(
        '-sd', '--send',
        help='Send command to blockchain',
        default=True)

    # withraw money from wallet
    subparser = sub2parsers.add_parser('transfer')
    subparser.add_argument(
        '-f', '--from_addr',
        help='From wallet address',
        default='EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs')
    subparser.add_argument(
        '-t', '--to_addr',
        help='To wallet address',
        required=True)
    subparser.add_argument(
        '-a', '--amount',
        help='Amount to send',
        type=int,
        required=True)
    subparser.add_argument(
        '-k', '--private_key',
        help='Private key file name',
        default='wallet.pk')
    subparser.add_argument(
        '-sd', '--send',
        help='Send command to blockchain',
        default=True)


def get_marketplace_args(subparsers):
    subparser = subparsers.add_parser('marketplace')
    sub2parsers = subparser.add_subparsers()

    # deploy new market
    subparser = sub2parsers.add_parser('new')    
    subparser.add_argument(
        '-f', '--wallet_addr',
        help='From wallet address',
        default='EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs')
    subparser.add_argument(
        '-k', '--private_key',
        help='Private key file name',
        default='wallet.pk')
    subparser.add_argument(
        '-o', '--owner_addr',
        help='Owner address',
        default='EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs')
    subparser.add_argument(
        '-i', '--init_ng',
        help='Amount init contract',
        type=int,
        default=50_000_000)
    subparser.add_argument(
        '-sd', '--send',
        help='Send command to blockchain',
        default=True)


def get_collection_args(subparsers):
    subparser = subparsers.add_parser('collection')
    sub2parsers = subparser.add_subparsers()

    # deploy new collection
    subparser = sub2parsers.add_parser('deploy')
    subparser.add_argument(
        '-s', '--seed',
        help='Collection seed',
        type=int,
        required=True)
    subparser.add_argument(
        '-f', '--wallet_addr',
        help='From wallet address',
        default='EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs')
    subparser.add_argument(
        '-o', '--owner_addr',
        help='Owner address',
        default='EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs')
    subparser.add_argument(
        '-r', '--royalty_addr',
        help='Royalty address',
        default='EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs')
    subparser.add_argument(
        '-k', '--private_key',
        help='Private key file name',
        default='wallet.pk')
    subparser.add_argument(
        '-i', '--init_ng',
        help='Amount init contract',
        type=int,
        default=50_000_000)
    subparser.add_argument(
        '-sd', '--send',
        help='Send command to blockchain',
        default=True)

    # get collection info
    subparser = sub2parsers.add_parser('info')
    subparser.add_argument(
        '-a', '--addr',
        help='Collection address',
        required=True)


def get_item_args(subparsers):
    subparser = subparsers.add_parser('item')
    sub2parsers = subparser.add_subparsers()

    # mint new item
    subparser = sub2parsers.add_parser('mint')
    subparser.add_argument(
        '-f', '--wallet_addr',
        help='From wallet address',
        default='EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs')
    subparser.add_argument(
        '-o', '--owner_addr',
        help='Owner address',
        default='EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs')
    subparser.add_argument(
        '-c', '--coll_addr',
        help='Collection address',
        required=True)
    subparser.add_argument(
        '-k', '--private_key',
        help='Private key file name',
        default='wallet.pk')
    subparser.add_argument(
        '-i', '--index',
        help='NFT item index',
        type=int,
        required=True)
    subparser.add_argument(
        '-ci', '--coll_ng',
        help='Amount to pass to collection contract',
        type=int,
        default=70_000_000)
    subparser.add_argument(
        '-ii', '--init_ng',
        help='Amount init contract',
        type=int,
        default=50_000_000)
    subparser.add_argument(
        '-sd', '--send',
        help='Send command to blockchain',
        default=True)

    # transfer NFT item to new owner
    subparser = sub2parsers.add_parser('transfer')
    subparser.add_argument(
        '-a', '--addr',
        help='NFT item address',
        required=True)
    subparser.add_argument(
        '-t', '--to_addr',
        help='New owner address',
        required=True)
    subparser.add_argument(
        '-f', '--wallet_addr',
        help='From wallet address',
        default='EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs')
    subparser.add_argument(
        '-k', '--private_key',
        help='Private key file name',
        default='wallet.pk')
    subparser.add_argument(
        '-fi', '--forw_ng',
        help='Amount to pass to collection contract',
        type=int,
        default=50_000_000)
    subparser.add_argument(
        '-ii', '--item_ng',
        help='Operation amount',
        type=int,
        default=80_000_000)
    subparser.add_argument(
        '-sd', '--send',
        help='Send command to blockchain',
        default=True)

    # get NFT item info
    subparser = sub2parsers.add_parser('info')
    subparser.add_argument(
        '-a', '--addr',
        help='NFT item address',
        required=True)


def get_auction_args(subparsers):
    subparser = subparsers.add_parser('auction')
    sub2parsers = subparser.add_subparsers()

    # get auction info
    subparser = sub2parsers.add_parser('info')
    subparser.add_argument(
        '-a', '--addr',
        help='Auction address',
        required=True)

    # deploy new auction
    subparser = sub2parsers.add_parser('new')
    subparser.add_argument(
        '-s', '--seed',
        help='Auction seed',
        required=True)
    subparser.add_argument(
        '-f', '--wallet_addr',
        help='From wallet address',
        default='EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs')
    subparser.add_argument(
        '-m', '--market_addr',
        help='Marketplace address',
        default='EQDY2SwQsRuFa_JJZkVMiUtCXh7Eld35lGNLU8kqjlrhRQAW')
    subparser.add_argument(
        '-i', '--item_addr',
        help='NFT item address',
        required=True)
    subparser.add_argument(
        '-mn', '--market_num',
        help='Marketplace fee numerator',
        type=int,
        default=10)
    subparser.add_argument(
        '-md', '--market_den',
        help='Marketplace fee denumerator',
        type=int,
        default=100)
    subparser.add_argument(
        '-r', '--royalty_addr',
        help='Royalty address',
        default='EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs')
    subparser.add_argument(
        '-rn', '--royalty_num',
        help='Royalty fee numerator',
        type=int,
        default=5)
    subparser.add_argument(
        '-rd', '--royalty_den',
        help='Royalty fee denumerator',
        type=int,
        default=100)
    subparser.add_argument(
        '-af', '--auc_fin',
        help='Auction deadline time',
        type=int,
        default=None)
    subparser.add_argument(
        '-sb', '--snip_before',
        help='Sniper before deadline (min)',
        type=int,
        default=5)
    subparser.add_argument(
        '-sa', '--snip_after',
        help='Sniper after deadline (min)',
        type=int,
        default=10)
    subparser.add_argument(
        '-mnb', '--min_bid',
        help='Min bid',
        type=int,
        default=1_000_000_000)
    subparser.add_argument(
        '-mxb', '--max_bid',
        help='Max bid (nullable))',
        type=int,
        default=5_000_000_000)
    subparser.add_argument(
        '-bs', '--bid_step',
        help='Bid step',
        type=int,
        default=500_000_000)
    subparser.add_argument(
        '-k', '--private_key',
        help='Private key file name',
        default='wallet.pk')
    subparser.add_argument(
        '-ii', '--init_ng',
        help='Amount init contract',
        type=int,
        default=50_000_000)
    subparser.add_argument(
        '-sd', '--send',
        help='Send command to blockchain',
        default=True)

    # start deployed auction
    subparser = sub2parsers.add_parser('start')
    subparser.add_argument(
        '-a', '--addr',
        help='Auction address',
        required=True)
    subparser.add_argument(
        '-ii', '--item_ng',
        help='Amount init contract',
        type=int,
        default=80_000_000)
    subparser.add_argument(
        '-fi', '--forw_ng',
        help='Amount to forward',
        type=int,
        default=50_000_000)
    subparser.add_argument(
        '-f', '--wallet_addr',
        help='From wallet address',
        default='EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs')
    subparser.add_argument(
        '-k', '--private_key',
        help='Private key file name',
        default='wallet.pk')
    subparser.add_argument(
        '-sd', '--send',
        help='Send command to blockchain',
        default=True)

    # cancel started auction
    subparser = sub2parsers.add_parser('cancel')
    subparser.add_argument(
        '-a', '--addr',
        help='Auction address',
        required=True)
    subparser.add_argument(
        '-ci', '--cancel_ng',
        help='Amount init contract',
        type=int,
        default=150_000_000)
    subparser.add_argument(
        '-f', '--wallet_addr',
        help='From wallet address',
        default='EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs')
    subparser.add_argument(
        '-k', '--private_key',
        help='Private key file name',
        default='wallet.pk')
    subparser.add_argument(
        '-sd', '--send',
        help='Send command to blockchain',
        default=True)

    # finish started auction
    subparser = sub2parsers.add_parser('finish')
    subparser.add_argument(
        '-a', '--addr',
        help='Auction address',
        required=True)
    subparser.add_argument(
        '-fi', '--finish_ng',
        help='Amount init contract',
        type=int,
        default=150_000_000)
    subparser.add_argument(
        '-f', '--wallet_addr',
        help='From wallet address',
        default='EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs')
    subparser.add_argument(
        '-k', '--private_key',
        help='Private key file name',
        default='wallet.pk')
    subparser.add_argument(
        '-sd', '--send',
        help='Send command to blockchain',
        default=True)

    # make a bid
    subparser = sub2parsers.add_parser('bid')
    subparser.add_argument(
        '-a', '--addr',
        help='Auction address',
        required=True)
    subparser.add_argument(
        '-am', '--amount',
        help='Amount init contract',
        type=int,
        default=150_000_000)
    subparser.add_argument(
        '-b', '--bidder_addr',
        help='Bidder wallet address',
        required=True)
    subparser.add_argument(
        '-k', '--private_key',
        help='Private key file name',
        default='wallet.pk')
    subparser.add_argument(
        '-sd', '--send',
        help='Send command to blockchain',
        default=True)


def get_cli_args(args):
    """Parse CLI arguments for get auction command arguments."""
    parser = argparse.ArgumentParser(
        description='NFT Auction Python API',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    subparsers = parser.add_subparsers()

    get_wallet_args(subparsers)
    get_marketplace_args(subparsers)
    get_collection_args(subparsers)
    get_item_args(subparsers)
    get_auction_args(subparsers)

    return vars(parser.parse_args(args))


def main(area, command, **kwargs):
    if area == 'wallet':
        run_wallet(command, **kwargs)
    elif area == 'marketplace':
        run_marketplace(command, **kwargs)
    elif area == 'collection':
        run_collection(command, **kwargs)
    elif area == 'item':
        run_item(command, **kwargs)
    elif area == 'auction':
        run_auction(command, **kwargs)
    else:
        raise Exception(f'Unknown area {area}')


if __name__ == '__main__':
    print('\n\nRunning Auction Python API...\n\n')
    kwargs_cli = get_cli_args(sys.argv[1:])
    main(sys.argv[1], sys.argv[2], **kwargs_cli)
