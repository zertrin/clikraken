# Samples

## buy\_and\_move.py

Python script to do a DCA transaction:

- buy a fixed amount of crypto.
- transfer the crypto to a known address (need the withdrawal
  authorization on your token/key).

Example:
```
$ ./buy_and_move.py 1000 EUR XBT hw_wallet
```

The state is kept in `dca.json` and removed once the transaction is
finished. The command can be interrupted a relaunched later.

The fees are computed only for EUR and XBT. Adapt to your needs.
