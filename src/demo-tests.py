import sys
import argparse

from tests.integration.tasks.wallet import run_wallet
from tests.integration.tasks.marketplace import run_marketplace
from tests.integration.tasks.collection import run_collection


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
        help='Wallet seed',
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
        '-r', '--royalty_address',
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

    # deploy new collection
    subparser = sub2parsers.add_parser('info')
    subparser.add_argument(
        '-a', '--addr',
        help='Collection address',
        required=True)


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

    return vars(parser.parse_args(args))


def main(area, command, **kwargs):
    if area == 'wallet':
        run_wallet(command, **kwargs)
    elif area == 'marketplace':
        run_marketplace(command, **kwargs)
    elif area == 'collection':
        run_collection(command, **kwargs)
    else:
        raise Exception(f'Unknown area {area}')


if __name__ == '__main__':
    print('\n\nRunning Auction Python API...\n\n')
    kwargs_cli = get_cli_args(sys.argv[1:])
    main(sys.argv[1], sys.argv[2], **kwargs_cli)
