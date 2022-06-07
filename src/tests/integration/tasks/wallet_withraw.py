from tasks.consts import wallet


def main():
    wallet.transfer_money(to='EQBFC3N-lJCkoxdKTzL6SsIzDMz8_A5x1zo3hgLbraTTN0hB', 
                          amount=7_000_000_000,
                          send=True)


if __name__ == '__main__':
    main()
