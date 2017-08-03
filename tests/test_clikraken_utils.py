from clikraken import clikraken_utils


def test_asset_pair_short():
    assert 'ETHEUR' == clikraken_utils.asset_pair_short('XETHZEUR')
    assert 'ETHEUR' == clikraken_utils.asset_pair_short('ETHEUR')
    assert 'DASHEUR' == clikraken_utils.asset_pair_short('DASHEUR')
    assert 'DASHXBT' == clikraken_utils.asset_pair_short('DASHXBT')


def test_base_quote_short_from_asset_pair():
    assert 'ETH', 'EUR' == clikraken_utils.base_quote_short_from_asset_pair('XETHZEUR')
    assert 'BCH', 'USD' == clikraken_utils.base_quote_short_from_asset_pair('BCHUSD')
    assert 'DASH', 'EUR' == clikraken_utils.base_quote_short_from_asset_pair('DASHEUR')
    assert 'DASH', 'XBT' == clikraken_utils.base_quote_short_from_asset_pair('DASHXBT')
