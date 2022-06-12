# TON NFT Auction Demo

Demonstration can be done slightly better in [whales sandbox](https://sandbox.tonwhales.com/explorer), because it conveniently groups incoming and outgoing transactions and also displays exit error codes.

For convenience of testing some wallets are already deployed and supplied with test coins:

- [EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs](https://sandbox.tonwhales.com/explorer/address/EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs) - main wallet that sends all the command transactions to auction, marketplace et.
- [EQBFC3N-lJCkoxdKTzL6SsIzDMz8_A5x1zo3hgLbraTTN0hB](https://sandbox.tonwhales.com/explorer/address/EQBFC3N-lJCkoxdKTzL6SsIzDMz8_A5x1zo3hgLbraTTN0hB) - bidder #1 wallet
- [EQAJbWNw7QmNi3I2kAPGELcvc-u_LEVnSSee9KrsB23LbgwL](https://sandbox.tonwhales.com/explorer/address/EQAJbWNw7QmNi3I2kAPGELcvc-u_LEVnSSee9KrsB23LbgwL) - bidder #2 wallet

All the wallets have the same private key ``secrets/wallet.pk``.

OK, let's get started 🦕.
Let's create an NFT item, auction and try to place some bids.

``>  cd src/``

Below is step-by-step demo guide.

### 1. Create an NFT collection:

``>  python3 -m demo-tests collection deploy --seed 12345``

Change seed to get other collections.

![](coll-deploy.png)

Check that the collection was deployed normally by invoke its contract get method (use your collection's address):

``>  python3 -m demo-tests collection info --addr EQCkqt2qxocFCSxntUVWkzNpM_jRReCNVtaY47QQtNW4VEvK``

![](coll-info.png)

### 2. Mint NFT Item

The following command will deploy NFT from previously created collection with appropriate index: 

``>  python3 -m demo-tests item mint --coll_addr EQCkqt2qxocFCSxntUVWkzNpM_jRReCNVtaY47QQtNW4VEvK --index 0``

![](item-mint.png)

Count to 10 and check NFT info (use your address of newly minted NFT):

``>  python3 -m demo-tests item info --addr EQAKX9FaRnupng_-Qi2QpvYzYsA_DKXh7MiaTikyx5aodS90``

![](item-info.png)

### 3. Use NFT marketplace:

Marketplace with default parameter is already deployed to Whales sandbox: 
https://sandbox.tonwhales.com/explorer/address/EQDY2SwQsRuFa_JJZkVMiUtCXh7Eld35lGNLU8kqjlrhRQAW
so one can simply use ``EQDY2SwQsRuFa_JJZkVMiUtCXh7Eld35lGNLU8kqjlrhRQAW`` address without deploying new one.

### 4. Deploy new auction!

By now we have an NFT ``EQAKX9FaRnupng_-Qi2QpvYzYsA_DKXh7MiaTikyx5aodS90`` from 2 and markeplace from 3. Let's deploy new auction by running command

``>  python3 -m demo-tests auction new --seed 12345 --item EQAKX9FaRnupng_-Qi2QpvYzYsA_DKXh7MiaTikyx5aodS90``

Check auction info after some time:

``>  python3 -m demo-tests auction info --addr EQAkZY7zoqEi_GhydU2reugEPixy5MNWHZ02Kmci4HRmVEAZ``

![](auction-deployed.png)

One can see that ``'nft_owner_address': None``. It means that auction was deployed by marketplace but not initialized by its NFT yet.
Let's get do it.

### 5. Start auction

Let's start deployed auction by send message from NFT to auction by the following CLI command:

``>  python3 -m demo-tests auction start --addr EQAkZY7zoqEi_GhydU2reugEPixy5MNWHZ02Kmci4HRmVEAZ``

Check auction info after some time:

``>  python3 -m demo-tests auction info --addr EQAkZY7zoqEi_GhydU2reugEPixy5MNWHZ02Kmci4HRmVEAZ``

![](auction-started.png)

Here we see ``'nft_owner_address': EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs`` which means that NFT has approved the auction and it's started.

### 6. Cancel auction

Before try to make any bids let's try cancel newly created auction.
This can be simply done by a command

``>  python3 -m demo-tests auction cancel --addr EQAkZY7zoqEi_GhydU2reugEPixy5MNWHZ02Kmci4HRmVEAZ``

Let's check auction info:

``>  python3 -m demo-tests auction info --addr EQAkZY7zoqEi_GhydU2reugEPixy5MNWHZ02Kmci4HRmVEAZ``

![](auction-cancelled.png)

Yep, it is cancelled, finished and can not be re-opened any more. Also note that NFT was returned to its previous owner:

``>  python3 -m demo-tests item info --addr EQAKX9FaRnupng_-Qi2QpvYzYsA_DKXh7MiaTikyx5aodS90``

``'owner_address': 'EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs'``

### 7. Create new auction and place a bid

Let's create another auction for the same NFT (please note different auction seed below):

``>  python3 -m demo-tests auction new --seed 67890 --item EQAKX9FaRnupng_-Qi2QpvYzYsA_DKXh7MiaTikyx5aodS90``

``Auction address: EQDtS4K3ZJDknk7lG9fc3RkntdUyVfCKBvaXBblBLoqAIxfR``

Start newly created auction:

``>  python3 -m demo-tests auction start --addr EQDtS4K3ZJDknk7lG9fc3RkntdUyVfCKBvaXBblBLoqAIxfR``

It's time to place a bid 💸. 
Bid can be done as a simple transaction with sufficient amount.
Here for convenience we will use the same python CLI as before.

Let's place a bid of 2 TON from default wallet ``EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs`` (It's also NFT owner address, but who cares - we can do so).

``>  python3 -m demo-tests auction bid --addr EQDtS4K3ZJDknk7lG9fc3RkntdUyVfCKBvaXBblBLoqAIxfR --bidder_addr EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs --amount 2000000000``

Count to 10 and check auction's info:

``>  python3 -m demo-tests auction info --addr EQDtS4K3ZJDknk7lG9fc3RkntdUyVfCKBvaXBblBLoqAIxfR``

Here we can see our current bid:

``'curr_winner_address': 'EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs',``
``'curr_winner_bid': 1950000000,``

The bid set is slightly less than 2 TON due to commissions.
Great! Let's place another one.

### 8. Place an overbid

Let's place another bid thar overbids previos one. Use another default wallet, say ``EQBFC3N-lJCkoxdKTzL6SsIzDMz8_A5x1zo3hgLbraTTN0hB``.

``>  python3 -m demo-tests auction bid --addr EQDtS4K3ZJDknk7lG9fc3RkntdUyVfCKBvaXBblBLoqAIxfR --bidder_addr EQBFC3N-lJCkoxdKTzL6SsIzDMz8_A5x1zo3hgLbraTTN0hB --amount 3000000000``

Auction info says that now we have another current winner

``'curr_winner_address': 'EQBFC3N-lJCkoxdKTzL6SsIzDMz8_A5x1zo3hgLbraTTN0hB',``
``'curr_winner_bid': 2950000000,``

which is correct.


We can also  check the result in auction's wallet explorer: 
https://sandbox.tonwhales.com/explorer/address/EQDtS4K3ZJDknk7lG9fc3RkntdUyVfCKBvaXBblBLoqAIxfR

![](return-bid.png)

which tells us that previous bid has been returned to previous bidder. Great!

### 9. Place an underbid

It is neccesary to know that one must overbid not only visible current value but also fome auction fees. Current bid is 2950000000 nTON. If one wants to overbid this bid he must bid not less than

2950000000 + bid_step + min_gas_amount() + min_tons_for_storage() + transfer_invoke_fee() + 4*fwd_fee
royalty_amount + marketplace_fee

which is approximately equals to 360000000 nTON. Let's bid amount less than that:

``>  python3 -m demo-tests auction bid --addr EQDtS4K3ZJDknk7lG9fc3RkntdUyVfCKBvaXBblBLoqAIxfR --bidder_addr EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs --amount 3150000000``

The bid returns to bidder except some fees:

https://sandbox.tonwhales.com/explorer/address/EQBR94p4TAivOi9mpGIoi-U2OH_TwuP01GfBtXf9QLMt_xBs

![](reject-bid.png)

### 10. Finish Auction

Finally, let's finish our auction.
Simply execue the command

``>  python3 -m demo-tests auction finish --addr EQDtS4K3ZJDknk7lG9fc3RkntdUyVfCKBvaXBblBLoqAIxfR``

![](auction-finish.png)

Great 🥳🎉🎊! All the fees are payed. Also note that auction has positive balance > 0.13 TON which is sufficient to cover it's storage fees for a years.

All other use-cases (anti-sniping, auction finishing by deadline etc.) can also be done this way.
